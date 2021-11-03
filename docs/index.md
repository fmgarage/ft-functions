---
title: Home
nav_order: 1
---

## Welcome to FX_Reports

FX_Reports is a powerful extension for genererating fully-featured spreadsheets in xslx format from FileMaker. It can easily be integrated into you existing solution.

### What can it do?

Exports from a FileMaker database are extremely quick to set up but also very limited – think of human readable column headers for instance. On the other end there is [LibXL](https://www.libxl.com) via the [MBS plugin](https://www.mbsplugins.eu/component_XL.shtml) where you can (and have to!) define every single detail of every cell that you want to put into your Excel file.

FX_Reports combines both the simplicity and flexibility into a single tool. You can use JSON to define the structure and content of your output file. For instance changing the column headers of a previously exported file looks something like this:

```json
{ "rows": [
    {"values": [ "First Name", "Last Name", "Age" ]},
    {"path": "desktop/contacts.xlsx"}
]}
```

Most of the Excel features are already supported, like

- multiple sheets
- formatting of text, numbers, dates etc.
- images

We will constantly improve the functionality of FX_Reports, so if you have a feature request, feel free to add or comment on an issue [here](https://github.com/fmgarage/fx-reports/labels/enhancement) 






following the golden rule *“Simple things should be simple, complex things should be possible”* (Alan Kay). This is accomplished by a

### What's in the Pipeline?

#### Formats

Integration into your existing solution will be even easier with formats.

This will also include support for native outputs

#### Queries

#### DynaPDF

Using a JSON schema as a meta format for describing and generating complex PDF documents using a similar approach like for Excel.

#### Word






### Support or Contact

Having trouble with implementing FX_Reports? Not sure, if FX_Reports matches your individual requirements? We are happy to assist, just contact us via our website, Twitter ([@fmgarage](https://twitter.com/fmgarage)) or email (support@fmgarage.com). 
