#!/usr/bin/env python

import os

from app                        import create_app, db
from app.models                 import AnUser, ARole, AnAuthor, APublication

from flask.ext.script           import Manager, Shell
from flask.ext.migrate          import Migrate, MigrateCommand
from flask_admin                import Admin
from flask_admin.contrib.sqla   import ModelView

app     = create_app( os.getenv( "FLASK_CONFIG" ) or "default" )
admin   = Admin( app, name="Bookshelf" )
admin.add_view( ModelView( AnAuthor, db.session ) )
admin.add_view( ModelView( APublication, db.session ) )
manager = Manager( app )
migrate = Migrate( app, db )

def MakeShellContext():
    return dict(
        app=app,
        db=db,
        AnUser=AnUser,
        ARole=ARole,
        AnAuthor=AnAuthor,
        APublication=APublication
)

manager.add_command( "shell", Shell( make_context=MakeShellContext ) )
manager.add_command( "db", MigrateCommand )

if __name__ == '__main__':
    manager.run()
