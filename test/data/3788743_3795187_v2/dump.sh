#/bin/bash

pg_dump -U statsbomb -h localhost "test_3788743_3795187_v2" > ./db.sql