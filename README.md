# py-ancient-jira-migration-tool
These Python scripts will help you migrate project issues and attachments from a very old version of JIRA (3.13.2-#335).

## Synopsis

There are two programs: one for scraping JIRA attachments using Selenium Webdriver and another for extracting project XML files into CSVs that can be loadeed into JIRA using the CSV import tool.

## Usage

Choose a project and enter the project suffix into the Attachment Scraper.  Then run the XML Scraper.

## Motivation

These scripts were written to migrate a very old JIRA installation into the latest version of JIRA without having to upgrade to every sub-version of JIRA in between.

## Installation

Requires several package imports including selenium webdriver, sys, os, time, autoIT, shutil, and csv.  Uses the element tree packages to parse XML.
