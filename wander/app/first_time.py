import os, imp
from wander.app import app, db
from migrate.versioning import api

def is_sqlite():
    return app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite://")

def create():
    db.create_all()

    if is_sqlite():
        if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
            api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
            api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
        else:
            api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'], api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))

def migrate():
    migration = app.config['SQLALCHEMY_MIGRATE_REPO'] + '/versions/%03d_migration.py' % (api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO']) + 1)
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'], tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO']))

def upgrade():
    api.upgrade(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
    print 'Current database version: ' + str(api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO']))

def downgrade():
    v = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
    api.downgrade(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'], v - 1)
    print 'Current database version: ' + str(api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO']))

def purge():
    for root, dirs, files in os.walk(app.config['SQLALCHEMY_MIGRATE_REPO'], topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(app.config['SQLALCHEMY_MIGRATE_REPO'])
    if is_sqlite():
        os.remove(app.config['SQLALCHEMY_DATABASE_URI'][len("sqlite:///"):])


