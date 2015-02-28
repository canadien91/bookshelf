# coding: utf-8

import os

basedir = os.path.abspath( os.path.dirname( __file__ ) )

class AConfig:
    SECRET_KEY                      = os.environ.get( "SECRET_KEY" ) or "BrainFart"
    SQLALCHEMY_COMMIT_ON_TEARDOWN   = True

    @staticmethod
    def init_app( app ):
        pass

class ADevelopmentConfig( AConfig ):
    DEBUG                   = True
    SQLALCHEMY_DATABASE_URI = os.environ.get( "DEV_DATABASE_URL" ) or \
        "sqlite:///" + os.path.join( basedir, "data-dev.sqlite" )

class ATestingConfig( AConfig ):
    TESTING                 = True
    SQLALCHEMY_DATABASE_URI = os.environ.get( "TEST_DATABASE_URL" ) or \
        "sqlite:///" + os.path.join( basedir, "data-test.sqlite" )


config = {
    "development"   : ADevelopmentConfig,
    "testing"       : ATestingConfig,

    "default"       : ADevelopmentConfig,
}
