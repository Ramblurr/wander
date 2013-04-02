#!/usr/bin/env python
import os
import glob
import imp
import argparse

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from migrate.versioning import api

def create():
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

def migrate():
    migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    a = api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def downgrade():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def purge():
    for root, dirs, files in os.walk(SQLALCHEMY_MIGRATE_REPO, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
        if SQLALCHEMY_DATABASE_URI.startswith("sqlite:///"):
            os.remove(SQLALCHEMY_DATABASE_URI[len("sqlite:///"):])



def _main():
    parser = argparse.ArgumentParser(description="sql alchemy database util")
    sp = parser.add_subparsers()
    sp_create = sp.add_parser('create', help='Create the database')
    sp_migrate = sp.add_parser('migrate', help='Migrate the database')
    sp_upgrade = sp.add_parser('upgrade', help='Upgrade the database')
    sp_downgrade = sp.add_parser('downgrade', help='Downgrade the database')
    sp_purge = sp.add_parser('purge', help='Purge the database')

    sp_create.set_defaults(func=create)
    sp_migrate.set_defaults(func=migrate)
    sp_upgrade.set_defaults(func=upgrade)
    sp_downgrade.set_defaults(func=downgrade)
    sp_purge.set_defaults(func=purge)

    args = parser.parse_args()
    args.func()

if __name__ == '__main__':
    _main()
