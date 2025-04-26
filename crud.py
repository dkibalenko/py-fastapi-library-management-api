from typing import List

from sqlalchemy.orm import Session

import models, schemas


def get_author_by_name(
        db: Session,
        name: str
) -> models.Author | None:
    """
    Retrieve an author by name from the database.

    Args:
    - db (Session): SQLAlchemy database session.
    - name (str): The name of the author to be retrieved.

    Returns:
    - models.Author | None: The retrieved author if found, otherwise None.
    """
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """
    Create a new author in the database.

    Args:
    - db (Session): SQLAlchemy database session.
    - author (schemas.AuthorCreate): The author to be created.

    Returns:
    - models.Author: The created author.
    """
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int, limit: int) -> List[models.Author]:
    """
    Validate and create Pydantic models from the retrieved list of SQlAlchemy 
    Author ORM objects out of the database.

    Parameters:
    - db (Session): SQLAlchemy database session.
    - skip (int): The number of records to skip for pagination.
    - limit (int): The maximum number of records to return.

    Returns:
    - List[models.Author]: A list of Pydantic models representing authors 
    after applying the specified pagination.
    """

    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return [schemas.Author.model_validate(author) for author in authors]


def get_author(db: Session, author_id: int) -> models.Author | None:
    """
    Retrieve an author by ID from the database.

    Args:
    - db (Session): SQLAlchemy database session.
    - author_id (int): The ID of the author to be retrieved.

    Returns:
    - models.Author | None: The retrieved author if found, otherwise None.
    """
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
