from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
deputado = Table('deputado', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nome', VARCHAR(length=50)),
    Column('partido', VARCHAR(length=10)),
    Column('email', VARCHAR(length=50)),
    Column('profissao', VARCHAR(length=60)),
    Column('telefone', VARCHAR(length=20)),
    Column('biografia', VARCHAR(length=300)),
)

projeto = Table('projeto', pre_meta,
    Column('numero', VARCHAR(length=20), primary_key=True, nullable=False),
    Column('nome', VARCHAR(length=50)),
    Column('texto', VARCHAR(length=200)),
    Column('status', VARCHAR(length=10)),
    Column('dataPublicacao', DATETIME),
    Column('deputado_id', INTEGER),
)

deputy = Table('deputy', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('party', String(length=10)),
    Column('email', String(length=50)),
    Column('job', String(length=60)),
    Column('phone', String(length=20)),
    Column('bio', String(length=300)),
)

project = Table('project', post_meta,
    Column('number', String(length=20), primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('text', String(length=200)),
    Column('status', String(length=10)),
    Column('publishDate', DateTime),
    Column('votesYes', Integer),
    Column('votesNo', Integer),
    Column('deputy_id', Integer),
)

votes = Table('votes', post_meta,
    Column('user_id', Integer),
    Column('project_number', String(length=20)),
    Column('voted_yes', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['deputado'].drop()
    pre_meta.tables['projeto'].drop()
    post_meta.tables['deputy'].create()
    post_meta.tables['project'].create()
    post_meta.tables['votes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['deputado'].create()
    pre_meta.tables['projeto'].create()
    post_meta.tables['deputy'].drop()
    post_meta.tables['project'].drop()
    post_meta.tables['votes'].drop()
