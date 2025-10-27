# GitCubby

## Introduction

The goal of this project is to create a easy to launch and run git server container. This server is not meant ot be full featured like projects like forgejo but easy to launch and configure through environment variables and config files requiring no ui configuration.

## Features

Access over HTTP for authenitcate push and pull as well as unauthenticated pull for selected repositories. Authencticated SSH push and pull for all repositories. Simple backup and recovery process built on duplicity. BAsic git-shell setup to manage the platform.

## Limitations

This will not support clear multiuser environments. There is limited user seperation but users are not intended to setup their own repos and there are simply public and private repos. Public repos have unautheticated http pull allowing for use in local automations easily without needed complex key management. Push access is authenticated on all repos. This does mean that more sensitive projects can be kept locally authenticated, but that all users who have user accounts/ssh keys to the system can access all repos  (no user segregation).

## Deployment

