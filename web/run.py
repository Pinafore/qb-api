import click
from app import run, server, db
import database


@click.group()
def cli():
    pass

@cli.command()
def run_web():
    run()

@cli.command()
def create_user():
    user = database.User(email='test@test.com', api_key='key')
    db.session.add(user)
    db.session.commit()

@cli.command()
def init_db():
    db.drop_all()
    db.create_all()
    database.load_questions()

if __name__ == '__main__':
    cli()
