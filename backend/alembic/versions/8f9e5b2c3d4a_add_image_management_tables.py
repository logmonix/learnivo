"""Add image management tables

Revision ID: 8f9e5b2c3d4a
Revises: 47e7404de0e1
Create Date: 2025-11-24 21:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8f9e5b2c3d4a'
down_revision: Union[str, Sequence[str], None] = '47e7404de0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create images table
    op.create_table('images',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('uploaded_by', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('filename')
    )
    
    # Create indexes for images table
    op.create_index('ix_images_uploaded_by', 'images', ['uploaded_by'])
    op.create_index('ix_images_created_at', 'images', ['created_at'])
    
    # Create chapter_images association table
    op.create_table('chapter_images',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('chapter_id', sa.UUID(), nullable=False),
        sa.Column('image_id', sa.UUID(), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for chapter_images table
    op.create_index('ix_chapter_images_chapter_id', 'chapter_images', ['chapter_id'])
    op.create_index('ix_chapter_images_image_id', 'chapter_images', ['image_id'])
    op.create_index('ix_chapter_images_display_order', 'chapter_images', ['chapter_id', 'display_order'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_chapter_images_display_order', table_name='chapter_images')
    op.drop_index('ix_chapter_images_image_id', table_name='chapter_images')
    op.drop_index('ix_chapter_images_chapter_id', table_name='chapter_images')
    op.drop_index('ix_images_created_at', table_name='images')
    op.drop_index('ix_images_uploaded_by', table_name='images')
    
    # Drop tables
    op.drop_table('chapter_images')
    op.drop_table('images')
