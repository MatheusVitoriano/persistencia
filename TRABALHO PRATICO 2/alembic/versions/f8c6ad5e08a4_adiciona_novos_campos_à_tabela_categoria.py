from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# Identificadores de revisão
revision = 'f8c6ad5e08a4'
down_revision = 'a05b0cdad49f'
branch_labels = None
depends_on = None

def column_exists(table_name, column_name):
    # Verifica se a coluna existe na tabela
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade():
    # Verifica se a coluna 'ativo' já existe antes de adicioná-la
    if not column_exists('categorias', 'ativo'):
        op.add_column('categorias', sa.Column('ativo', sa.Boolean(), nullable=True))

def downgrade():
    # Remove a coluna 'ativo' caso ela exista
    if column_exists('categorias', 'ativo'):
        op.drop_column('categorias', 'ativo')
