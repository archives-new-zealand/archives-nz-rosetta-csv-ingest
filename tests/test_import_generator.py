"""Archives NZ import generator tests."""

# pylint: disable=C0103

from typing import Final

from src.anz_rosetta_csv.rosetta_csv_generator import RosettaCSVGenerator

schema: Final[
    str
] = """{
    "title": "Rosetta CSV Validation Schema - Archives NZ",
    "description": "Draft schema for validating CSV files for ingest in Rosetta at Archives New Zealand.",
	"validator": "http://csvlint.io/",
	"standard" : "http://dataprotocols.org/json-table-schema/",
    "fields": [
        {
            "name": "Object Type",
            "description": "The type of object we're describing in the row.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": true,
                "pattern": "^(SIP|IE|REPRESENTATION|FILE)$"
            }
        },
        {
            "name": "SIP Title",
            "description": "Title of the SIP to ingest.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Title (DC)",
            "description": "Title of the digital object being uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Access Rights Policy ID (IE)",
            "description": "Rosetta access restriction key.",
            "type": "http://www.w3.org/2001/XMLSchema#int",
            "constraints": {
                "required": false,
                "pattern": ""
            }
        },
        {
            "name": "Archway Unique ID (Object Identifier)",
            "description": "Record number in Archive New Zealand's catalogue.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": ""
            }
        },
        {
            "name": "Identifier - Archway Unique Id (DC)",
            "description": "Record number in Archive New Zealand's catalogue.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": ""
            }
        },
        {
            "name": "Archway Series Number",
            "description": "Series number identifier as denoted by Archive New Zealand's catalogue.",
            "type": "http://www.w3.org/2001/XMLSchema#int",
            "constraints": {
                "required": false,
                "pattern": ""
            }
        },
        {
            "name": "Provenance (dcterms)",
            "description": "Code for originating agency, e.g. Archives New Zealand: AEZB.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^[A-Z]{4}$|^$)"
            }
        },
        {
            "name": "IE Entity Type",
            "description": "Essence of the content found in the digital object.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(ANZ_NotDetermined)$|^$)"
            }
        },
        {
            "name": "Submission Reason",
            "description": "Overarching reason for submission into Rosetta, e.g. Digital Transfer.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(DigitalTransfer)$|^$)"
            }
        },
        {
            "name": "Event Identifier Type",
            "description": "Type of event ID we're assigning. This will always be EXTERNAL in CSV",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(EXTERNAL)$"
            }
        },
        {
            "name": "Event Identifier Value",
            "description": "Unique ID for the event for this object within this SIP. We can only have on event.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(EXT_1)$"
            }
        },
        {
            "name": "Event Type",
            "description": "Type of event we're documenting. This will always be CREATION at the moment in CSV.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(CREATION)$"
            }
        },
        {
            "name": "Event Description",
            "description": "Description of the event. Workarounds mean that this will always be Provenance Note catch-all in CSV.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(Provenance Note)$"
            }
        },
        {
            "name": "Event Date",
            "description": "Date the event happens. ISO8601: {YYYY-MM-DDThh:mm:ss}.",
            "type": "http://www.w3.org/2001/XMLSchema#dateTime",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Event Outcome1",
            "description": "Status of the outcome of the event happening. E.g. SUCCESS or FAILURE. Will always be SUCCESS.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(SUCCESS)$"
            }
        },
        {
            "name": "Event Outcome Detail1",
            "description": "Description of the event being listed under Provenance Note.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Event Outcome Detail Extension1",
            "description": "Additional information for description of the event being listed under Provenance Note.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Event Outcome2",
            "description": "Status of the outcome of the event happening. E.g. SUCCESS or FAILURE. Will always be SUCCESS.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(SUCCESS)$"
            }
        },
        {
            "name": "Event Outcome Detail2",
            "description": "Description of the event being listed under Provenance Note.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Event Outcome Detail Extension2",
            "description": "Additional information for description of the event being listed under Provenance Note.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Event Outcome3",
            "description": "Status of the outcome of the event happening. E.g. SUCCESS or FAILURE. Will always be SUCCESS.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "^(SUCCESS)$"
            }
        },
        {
            "name": "Event Outcome Detail3",
            "description": "Description of the event being listed under Provenance Note.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Event Outcome Detail Extension3",
            "description": "Additional information for description of the event being listed under Provenance Note.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },

        {
            "name": "Revision Number",
            "description": "Version of the file to be uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#int",
            "constraints": {
                "required": false,
                "pattern": "ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū"
            }
        },
        {
            "name": "Usage Type",
            "description": "What we can do with file instance in Rosetta, e.g. VIEW.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(VIEW)$|^$)"
            }
        },
        {
            "name": "Representation Code",
            "description": "Is this file a digital original?",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(True|False)$|^$)"
            }
        },
        {
            "name": "Preservation Type",
            "description": "Preservation purpose of file instance in Rosetta, e.g. Preservation Master.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(PRESERVATION_MASTER|DERIVATIVE_COPY)$|^$)"
            }
        },
        {
            "name": "Digital Original",
            "description": "Is this file a digital original?",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "File Original Path",
            "description": "Directory path to location of file to be uploaded. Path begins at root of ZIP and does not begin with an opening slash. Does not contain filename",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "File Original Name",
            "description": "File name, including extension, of file to be uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "File Label",
            "description": "File label as an alternative to name.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "MD5",
            "description": "Hash generated for the file to be uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": ""
            }
        },
        {
            "name": "File Modification Date (General File Characteristics)",
            "description": "Date file was last modified.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "File Creation Date (General File Characteristics)",
            "description": "Date file was created.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        }
    ]
}
"""

config: Final[
    str
] = """
[application configuration]

#if we're using a provenance note, we need to know the hash column (again!)
#so we use this value here
provhash = MD5

[rosetta mapping]
#rosetta field on the left, export field on the right

SIP Title=Accession test ingest WITH events

Title (DC)=Title
Archway Unique ID (Object Identifier)=Item Code
Identifier - Archway Unique Id (DC)=Item Code
Archway Series Number=Final Series
Provenance (dcterms)=Transferring Agency
Access Rights Policy ID (IE)=Restriction Status

[static values]
#values will just get transplanted into the SIP

IE Entity Type=ANZ_BornDigital
Submission Reason=DigitalTransfer
Revision Number=1
Usage Type=VIEW
Digital Original=TRUE
File Creation Date (General File Characteristics)=
Preservation Type=PRESERVATION_MASTER

#Access maps to next section to enable multiple access mappings
#Can also make static here...
#Access=
#Access Rights Policy ID (IE)=

#PROVENANCE
#IF YOU WANT YOU CAN ADD STATIC VALUES TO THE EVENT FIELDS HERE

[access values]
#Access maps to this section to enable multiple access mappings
O=1916130
M=1916131

[droid mapping]

File Original Name=NAME
File Original Path=FILE_PATH
File Modification Date (General File Characteristics)=LAST_MODIFIED
MD5=MD5_HASH

[path values]
pathmask=R:\\Digitised\\Wellington\\mock_transfer\\
subseriesmask=R:\\Digitised\\Wellington\\mock_transfer\\2006-2007

[rosetta csv fields]
CSVSECTIONS=IE,REPRESENTATION,FILE

IE = Title (DC),Access Rights Policy ID (IE),Archway Unique ID (Object Identifier),Identifier - Archway Unique Id (DC),Archway Series Number,Provenance (dcterms),IE Entity Type,Submission Reason,Event Identifier Type,Event Identifier Value,Event Type,Event Description,Event Date,Event Outcome1,Event Outcome Detail1,Event Outcome Detail Extension1,Event Outcome2,Event Outcome Detail2,Event Outcome Detail Extension2,Event Outcome3,Event Outcome Detail3,Event Outcome Detail Extension3
REPRESENTATION = Revision Number,Usage Type,Representation Code,Preservation Type,Digital Original
FILE = File Original Path,File Original Name,File Label,MD5,File Modification Date (General File Characteristics),File Creation Date (General File Characteristics)

"""

list_control: Final[
    str
] = """
Item Code,State,Missing,Missing Comment,Transferring Agency,Series,Container,Box Number,Item Number,Record Number,Part Number,Sep Flag,Sep Number,Sub-Series,Title,Open Year,Close Year,Restriction Status,Restriction Expires,Restriction Expiry Year,Preservation,Alternative Record Number,Former Archives Reference,Record Type,Description,Public View,PV Expiry,PV Expiry Year,Item Level,Accession Number,Repository Reference,Final Series,Location
R25437983,,,294c07b86ad9b460007d1655be2bbf38,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme,2006-07 Rule Programme – MoU invitation to submit,2006,2006,M,,,Issuable,,,Not Determined,Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters],Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437984,,,c5fb91dcd533576c357fe8e50fc399b7,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,2006-07 Rules Bid_ Letter,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437985,,,5961159db13aaca1ae111cf1b5b9bccd,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,2006-07_Rule Milestones,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437986,,,c1f0f5aed44d33cd3b30e1d3fa3c227d,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,2006-07_Rule Pricing v2,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437987,,,bb3e27fda4308e713a91903acd6c6880,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,2006-07_Rule Pricing,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437988,,,60332a7349c81a7ef4ea6012dec17326,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,2006-07_Rule Project Implications,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437989,,,109d9ce7d56802837fd171c3120ecd2b,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,2006-07_Rule Project Summaries,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437990,,,4dbab6726c35c85890d2d615b274686b,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,Provision Velodromes - NZTS Assessment,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437991,,,df672d996911f6237ad006928a42e1c0,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\2006-07 Project Programme Submission to MoU,Person Requirements - NZTS Assessment,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437992,,,9abff2bf06dc98c1e113061a279d9d4d,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme,Contract Document 06-07 Final Schedule 1 (2),2006,2006,O,,,Issuable,,,Not Determined,"Last Accessed: 2017, Last Save Date: 2006 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437993,,,34356f954f0f85a413ab2be1667abd57,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\MoU,Contract Compare 05-06 with 06-07,2007,2007,O,,,Issuable,,,Not Determined,"Last Save Date: 2007, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437994,,,9808f4d6789a114ccb854f5a6a3604fb,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\MoU,Draft Cabinet Paper 2024-07NZ4,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437995,,,a011256311cda2b4dd099fe1f002fca0,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\MoU,Rules management update,2007,2007,O,,,Issuable,,,Not Determined,Last Accessed: 2011,Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437996,,,3276c4b0710e86538bb2443170e4d2b6,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\Project Briefs,Assessemtn and Management of Velodrome Collision Risk_Rule Project Brief,2007,2007,O,,,Issuable,,,Not Determined,Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters],Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437997,,,335d130cd1930f225c087c381907f12c,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\Summary of Projects for Consideration,Current projects carried over to 1950-1965,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437998,,,5bb15dea7fe8e13d5c484b6c825b50ab,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\Summary of Projects for Consideration,Current projects due for completion before 2070-2071,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437999,,,076c7949bcf37db86b1dbf819148a6cd,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\Summary of Projects for Consideration,New projects under consideration for 2040-2600,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25438000,,,4e0ae8c50bc6ec6b59f114c07917f2f5,AAAA,26000,,,,,,,,Project Programme\2006-2007 Project Programme\\Summary of Projects for Consideration,New projects under consideration for 2040-2600_Comments,2007,2007,O,,,Issuable,,,Not Determined,"Last Save Date: 2007, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
"""

droid_csv: Final[
    str
] = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
2,0,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme,2006-2007 Rules Programme,,Done,,Folder,,2017-06-27T13:49:34,false,,,,,,
3,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07 Rule Programme – MoU invitation to submit.pdf,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rule Programme – MoU invitation to submit.pdf ,2006-07 Rule Programme – MoU invitation to submit.pdf,Signature,Done,228461,File,pdf,2006-02-13T10:45:40,false,294c07b86ad9b460007d1655be2bbf38,1,fmt/16,application/pdf,Acrobat PDF 1.2 - Portable Document Format,1.2
4,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT,2006-07 Rules Programme Submission to MoT,,Done,,Folder,,2017-07-20T11:32:23,false,,,,,,
5,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07%20Rules%20Bid_%20Letter.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\2006-07 Rules Bid_ Letter.doc ,2006-07 Rules Bid_ Letter.doc,Container,Done,29184,File,doc,2006-03-24T15:45:55,false,c5fb91dcd533576c357fe8e50fc399b7,1,fmt/40,application/msword,Microsoft Word Document,97-2003
6,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07_Rule%20Milestones.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\2006-07_Rule Milestones.doc ,2006-07_Rule Milestones.doc,Container,Done,50176,File,doc,2006-03-24T16:14:22,false,5961159db13aaca1ae111cf1b5b9bccd,1,fmt/40,application/msword,Microsoft Word Document,97-2003
7,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07_Rule%20Pricing%20v2.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\2006-07_Rule Pricing v2.doc,2006-07_Rule Pricing v2.doc,Container,Done,41984,File,doc,2006-08-11T16:25:34,false,c1f0f5aed44d33cd3b30e1d3fa3c227d,1,fmt/40,application/msword,Microsoft Word Document,97-2003
8,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07_Rule%20Pricing.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\2006-07_Rule Pricing.doc ,2006-07_Rule Pricing.doc,Container,Done,41984,File,doc,2006-03-09T13:33:16,false,bb3e27fda4308e713a91903acd6c6880,1,fmt/40,application/msword,Microsoft Word Document,97-2003
9,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07_Rule%20Project%20Implications%20.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\2006-07_Rule Project Implications .doc ,2006-07_Rule Project Implications .doc,Container,Done,28160,File,doc,2006-03-24T16:13:50,false,60332a7349c81a7ef4ea6012dec17326,1,fmt/40,application/msword,Microsoft Word Document,97-2003
10,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07_Rule%20Project%20Summaries.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\2006-07_Rule Project Summaries.doc ,2006-07_Rule Project Summaries.doc,Container,Done,43520,File,doc,2006-03-17T16:58:26,false,109d9ce7d56802837fd171c3120ecd2b,1,fmt/40,application/msword,Microsoft Word Document,97-2003
11,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/Provision%20Velodromes%20-%20NZTS%20Assessment.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\Provision Velodromes - NZTS Assessment.doc ,Provision Velodromes - NZTS Assessment.doc,Container,Done,43520,File,doc,2006-03-24T16:12:54,false,4dbab6726c35c85890d2d615b274686b,1,fmt/40,application/msword,Microsoft Word Document,97-2003
12,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/Person%20Requirements%20-%20NZTS%20Assessment.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\2006-07 Rules Programme Submission to MoT\\Person Requirements - NZTS Assessment.doc ,Person Requirements - NZTS Assessment.doc,Container,Done,43008,File,doc,2006-03-24T15:33:36,false,df672d996911f6237ad006928a42e1c0,1,fmt/40,application/msword,Microsoft Word Document,97-2003
13,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Contract%20Document%2006-07%20Final%20Schedule%201%20%282%29.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Contract Document 06-07 Final Schedule 1 (2).doc ,Contract Document 06-07 Final Schedule 1 (2).doc,Container,Done,56320,File,doc,2006-11-27T15:01:06,false,9abff2bf06dc98c1e113061a279d9d4d,1,fmt/40,application/msword,Microsoft Word Document,97-2003
14,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/MoU/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\MoT,MoT,,Done,,Folder,,2017-07-07T14:54:10,false,,,,,,
15,14,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/MoU/Contract%20Compare%2005-06%20with%2006-07.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\MoT\\Contract Compare 05-06 with 06-07.doc ,Contract Compare 05-06 with 06-07.doc,Container,Done,311296,File,doc,2007-03-02T14:32:51,false,34356f954f0f85a413ab2be1667abd57,1,fmt/40,application/msword,Microsoft Word Document,97-2003
16,14,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/MoU/Draft%20Cabinet%20Paper%202024-07NZ4.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\MoT\\,Draft Cabinet Paper 2024-07NZ4.doc,Container,Done,103936,File,doc,2006-04-27T13:52:23,false,9808f4d6789a114ccb854f5a6a3604fb,1,fmt/40,application/msword,Microsoft Word Document,97-2003
17,14,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/MoU/Rules%20management%20update.htm,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\MoT\\Rules management update.htm ,Rules management update.htm,Signature,Done,25557,File,htm,2007-01-23T14:41:46,false,a011256311cda2b4dd099fe1f002fca0,1,fmt/583,,Vector Markup Language,
18,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Project%20Briefs/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Project Briefs,Project Briefs,,Done,,Folder,,2017-06-27T13:49:34,false,,,,,,
19,18,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Project%20Briefs/Assessemtn%20and%20Management%20of%20Velodrome%20Collision%20Risk_Rule%20Project%20Brief.pdf,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Project Briefs\\Assessemtn and Management of Velodrome Collision Risk_Rule Project Brief.pdf ,Assessemtn and Management of Velodrome Collision Risk_Rule Project Brief.pdf,Signature,Done,3873,File,pdf,2007-02-01T11:13:11,false,3276c4b0710e86538bb2443170e4d2b6,1,fmt/17,application/pdf,Acrobat PDF 1.3 - Portable Document Format,1.3
20,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Summary%20of%20Projects%20for%20Consideration/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Summary of Projects for Consideration,Summary of Projects for Consideration,,Done,,Folder,,2017-06-27T13:49:34,false,,,,,,
21,20,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Summary%20of%20Projects%20for%20Consideration/Current%20projects%20carried%20over%20to%201950-1965.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Summary of Projects for Consideration\\Current projects carried over to 1950-1965.doc ,Current projects carried over to 1950-1965.doc,Container,Done,65024,File,doc,2006-02-15T16:52:19,false,335d130cd1930f225c087c381907f12c,1,fmt/40,application/msword,Microsoft Word Document,97-2003
22,20,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Summary%20of%20Projects%20for%20Consideration/Current%20projects%20due%20for%20completion%20before%202070-2071.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Summary of Projects for Consideration\\Current projects due for completion before 2070-2071.doc ,Current projects due for completion before 2070-2071.doc,Container,Done,45568,File,doc,2006-02-14T09:47:59,false,5bb15dea7fe8e13d5c484b6c825b50ab,1,fmt/40,application/msword,Microsoft Word Document,97-2003
23,20,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Summary%20of%20Projects%20for%20Consideration/New%20projects%20under%20consideration%20for%202040-2600.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Summary of Projects for Consideration\\New projects under consideration for 2040-2600.doc ,New projects under consideration for 2040-2600.doc,Container,Done,90112,File,doc,2006-02-14T16:24:48,false,076c7949bcf37db86b1dbf819148a6cd,1,fmt/40,application/msword,Microsoft Word Document,97-2003
24,20,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/Summary%20of%20Projects%20for%20Consideration/New%20projects%20under%20consideration%20for%202040-2600_Comments.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Rules Programme\\Summary of Projects for Consideration\\New projects under consideration for 2040-2600_Comments.doc ,New projects under consideration for 2040-2600_Comments.doc,Container,Done,74240,File,doc,2007-03-08T16:30:13,false,4e0ae8c50bc6ec6b59f114c07917f2f5,1,fmt/40,application/msword,Microsoft Word Document,97-2003

"""

prov: Final[
    str
] = """
RECORDNUMBER,NOTEDATE,NOTETEXT,ORIGINALNAME,CHECKSUM
R25437992,2017-10-27 12:51:00,File name changed,FixedFilename001 001,Ignore
R25437997,2017-10-27 12:55:00,File edited in MS Word,Ignore,f8c8983bf05854cae18328c6c2adb75e
"""

result: Final[
    str
] = """
"Object Type","Title (DC)","Title (DC)","Access Rights Policy ID (IE)","Archway Unique ID (Object Identifier)","Identifier - Archway Unique Id (DC)","Archway Series Number","Provenance (dcterms)","IE Entity Type","Submission Reason","Event Identifier Type","Event Identifier Value","Event Type","Event Description","Event Date","Event Outcome1","Event Outcome Detail1","Event Outcome Detail Extension1","Event Outcome2","Event Outcome Detail2","Event Outcome Detail Extension2","Event Outcome3","Event Outcome Detail3","Event Outcome Detail Extension3","Revision Number","Usage Type","Representation Code","Preservation Type","Digital Original","File Original Path","File Original Name","File Label","MD5","File Modification Date (General File Characteristics)","File Creation Date (General File Characteristics)"
"SIP","Accession test ingest WITH events","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""
"IE","","2006-07 Rule Programme – MoU invitation to submit","1916131","R25437983","R25437983","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/","2006-07 Rule Programme – MoU invitation to submit.pdf","","294c07b86ad9b460007d1655be2bbf38","2006-02-13T10:45:40",""
"IE","","2006-07 Rules Bid_ Letter","1916130","R25437984","R25437984","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","2006-07 Rules Bid_ Letter.doc","","c5fb91dcd533576c357fe8e50fc399b7","2006-03-24T15:45:55",""
"IE","","2006-07_Rule Milestones","1916130","R25437985","R25437985","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","2006-07_Rule Milestones.doc","","5961159db13aaca1ae111cf1b5b9bccd","2006-03-24T16:14:22",""
"IE","","2006-07_Rule Pricing v2","1916130","R25437986","R25437986","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","2006-07_Rule Pricing v2.doc","","c1f0f5aed44d33cd3b30e1d3fa3c227d","2006-08-11T16:25:34",""
"IE","","2006-07_Rule Pricing","1916130","R25437987","R25437987","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","2006-07_Rule Pricing.doc","","bb3e27fda4308e713a91903acd6c6880","2006-03-09T13:33:16",""
"IE","","2006-07_Rule Project Implications","1916130","R25437988","R25437988","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","2006-07_Rule Project Implications .doc","","60332a7349c81a7ef4ea6012dec17326","2006-03-24T16:13:50",""
"IE","","2006-07_Rule Project Summaries","1916130","R25437989","R25437989","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","2006-07_Rule Project Summaries.doc","","109d9ce7d56802837fd171c3120ecd2b","2006-03-17T16:58:26",""
"IE","","Provision Velodromes - NZTS Assessment","1916130","R25437990","R25437990","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","Provision Velodromes - NZTS Assessment.doc","","4dbab6726c35c85890d2d615b274686b","2006-03-24T16:12:54",""
"IE","","Person Requirements - NZTS Assessment","1916130","R25437991","R25437991","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/2006-07 Rules Programme Submission to MoT/","Person Requirements - NZTS Assessment.doc","","df672d996911f6237ad006928a42e1c0","2006-03-24T15:33:36",""
"IE","","Contract Document 06-07 Final Schedule 1 (2)","1916130","R25437992","R25437992","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","EXTERNAL","EXT_1","CREATION","Provenance Note","2017-10-27 12:51:00","SUCCESS","File name changed","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/","FixedFilename001 001","","9abff2bf06dc98c1e113061a279d9d4d","2006-11-27T15:01:06",""
"IE","","Contract Compare 05-06 with 06-07","1916130","R25437993","R25437993","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/MoT/","Contract Compare 05-06 with 06-07.doc","","34356f954f0f85a413ab2be1667abd57","2007-03-02T14:32:51",""
"IE","","Draft Cabinet Paper 2024-07NZ4","1916130","R25437994","R25437994","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/MoT/","Draft Cabinet Paper 2024-07NZ4.doc","","9808f4d6789a114ccb854f5a6a3604fb","2006-04-27T13:52:23",""
"IE","","Rules management update","1916130","R25437995","R25437995","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/MoT/","Rules management update.htm","","a011256311cda2b4dd099fe1f002fca0","2007-01-23T14:41:46",""
"IE","","Assessemtn and Management of Velodrome Collision Risk_Rule Project Brief","1916130","R25437996","R25437996","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/Project Briefs/","Assessemtn and Management of Velodrome Collision Risk_Rule Project Brief.pdf","","3276c4b0710e86538bb2443170e4d2b6","2007-02-01T11:13:11",""
"IE","","Current projects carried over to 1950-1965","1916130","R25437997","R25437997","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","EXTERNAL","EXT_1","CREATION","Provenance Note","2017-10-27 12:55:00","SUCCESS","File edited in MS Word","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/Summary of Projects for Consideration/","Current projects carried over to 1950-1965.doc","","f8c8983bf05854cae18328c6c2adb75e","2006-02-15T16:52:19",""
"IE","","Current projects due for completion before 2070-2071","1916130","R25437998","R25437998","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/Summary of Projects for Consideration/","Current projects due for completion before 2070-2071.doc","","5bb15dea7fe8e13d5c484b6c825b50ab","2006-02-14T09:47:59",""
"IE","","New projects under consideration for 2040-2600","1916130","R25437999","R25437999","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/Summary of Projects for Consideration/","New projects under consideration for 2040-2600.doc","","076c7949bcf37db86b1dbf819148a6cd","2006-02-14T16:24:48",""
"IE","","New projects under consideration for 2040-2600_Comments","1916130","R25438000","R25438000","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","PRESERVATION_MASTER","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Rules Programme/Summary of Projects for Consideration/","New projects under consideration for 2040-2600_Comments.doc","","4e0ae8c50bc6ec6b59f114c07917f2f5","2007-03-08T16:30:13",""
"""


def test_csv_generation(tmp_path):
    """Provide a full integration test for the code base."""

    tmp_dir = tmp_path / "test_ingest"
    tmp_dir.mkdir()
    config_file = tmp_dir / "config.cfg"
    schema_file = tmp_dir / "schema.json"
    droid_report = tmp_dir / "droid.csv"
    list_control_file = tmp_dir / "lc.csv"
    prov_file = tmp_dir / "prov.notes"

    config_file.write_text(config.strip().lstrip(), encoding="utf-8")
    schema_file.write_text(schema.strip().lstrip(), encoding="utf-8")
    droid_report.write_text(droid_csv.strip().lstrip(), encoding="utf-8")
    list_control_file.write_text(list_control.strip().lstrip(), encoding="utf-8")
    prov_file.write_text(prov.strip().lstrip(), encoding="utf-8")

    csvgen = RosettaCSVGenerator(
        droid_report,
        list_control_file,
        schema_file,
        config_file,
        prov_file,
    )
    res = csvgen.export_to_rosetta_csv()
    assert res.strip() == result.strip()


dupe_config: Final[
    str
] = """
[application configuration]

#if we're using a provenance note, we need to know the hash column (again!)
#so we use this value here
provhash = MD5

[rosetta mapping]
#rosetta field on the left, export field on the right

SIP Title=Duplicates Ingest

Title (DC)=Title
Archway Unique ID (Object Identifier)=Item Code
Identifier - Archway Unique Id (DC)=Item Code
Archway Series Number=Final Series
Provenance (dcterms)=Transferring Agency
Access Rights Policy ID (IE)=Restriction Status

[static values]
#values will just get transplanted into the SIP

IE Entity Type=ANZ_BornDigital
Submission Reason=DigitalTransfer
Revision Number=1
Usage Type=VIEW
Digital Original=TRUE
File Creation Date (General File Characteristics)=
Preservation Type=♙♘♗♖♕♔♚♛♜♝♞♟ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū ♭ ♮ ♯

#Access maps to next section to enable multiple access mappings
#Can also make static here...
#Access=
#Access Rights Policy ID (IE)=

#PROVENANCE
#IF YOU WANT YOU CAN ADD STATIC VALUES TO THE EVENT FIELDS HERE

[access values]
#Access maps to this section to enable multiple access mappings
O=1916130
M=1916131

[droid mapping]

File Original Name=NAME
File Original Path=FILE_PATH
File Modification Date (General File Characteristics)=LAST_MODIFIED
MD5=MD5_HASH

[path values]
pathmask=R:\\Digitised\\Wellington\\mock_transfer\\
subseriesmask=R:\\Digitised\\Wellington\\mock_transfer\\2006-2007

[rosetta csv fields]
CSVSECTIONS=IE,REPRESENTATION,FILE

IE = Title (DC),Access Rights Policy ID (IE),Archway Unique ID (Object Identifier),Identifier - Archway Unique Id (DC),Archway Series Number,Provenance (dcterms),IE Entity Type,Submission Reason,Event Identifier Type,Event Identifier Value,Event Type,Event Description,Event Date,Event Outcome1,Event Outcome Detail1,Event Outcome Detail Extension1,Event Outcome2,Event Outcome Detail2,Event Outcome Detail Extension2,Event Outcome3,Event Outcome Detail3,Event Outcome Detail Extension3
REPRESENTATION = Revision Number,Usage Type,Representation Code,Preservation Type,Digital Original
FILE = File Original Path,File Original Name,File Label,MD5,File Modification Date (General File Characteristics),File Creation Date (General File Characteristics)
"""

dupe_list_control: Final[
    str
] = """
Item Code,State,Missing,Missing Comment,Transferring Agency,Series,Container,Box Number,Item Number,Record Number,Part Number,Sep Flag,Sep Number,Sub-Series,Title,Open Year,Close Year,Restriction Status,Restriction Expires,Restriction Expiry Year,Preservation,Alternative Record Number,Former Archives Reference,Record Type,Description,Public View,PV Expiry,PV Expiry Year,Item Level,Accession Number,Repository Reference,Final Series,Location
R25437983,,,294c07b86ad9b460007d1655be2bbf38,AAAA,26000,,,,,,,,Project Programme,2006-07 Project Programme – MoU invitation to submit,2006,2006,O,,,Issuable,,,Not Determined,Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters],Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
R25437984,,,294c07b86ad9b460007d1655be2bbf38,AAAA,26000,,,,,,,,Project Programme\\2006-07 Project Programme Submission to MoU,2006-07 Rules Bid_ (🥬) Letter,2006,2006,O,,,Issuable,,,Not Determined,"Last Save Date: 2006, Last Accessed: 2017 * [Dates are generated from the file system and reflect file system parameters]",Y,,,Item,ANZ2600,ANZ2600-1,26000-1,Digital Repository
"""

dupe_droid_csv: Final[
    str
] = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
2,0,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Project Programme,2006-2007 Rules Programme,,Done,,Folder,,2017-06-27T13:49:34,false,,,,,,
3,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07 Rule Programme – MoU invitation to submit.pdf,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Project Programme\\2006-07 Project Programme – MoU invitation to submit.pdf ,2006-07 Project Programme – MoU invitation to submit.pdf,Signature,Done,228461,File,pdf,2006-02-13T10:45:40,false,294c07b86ad9b460007d1655be2bbf38,1,fmt/16,application/pdf,Acrobat PDF 1.2 - Portable Document Format,1.2
4,2,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Project Programme\\2006-07 Project Programme Submission to MoU,2006-07 Rules Programme Submission to MoT,,Done,,Folder,,2017-07-20T11:32:23,false,,,,,,
5,4,file:/R:/Digitised/Wellington/mock_transfer/2006-2007%20Project%20Programme/2006-07%20Project%20Programme%20Submission%20to%20MoU/2006-07%20Rules%20Bid_%20Letter.doc,R:\\Digitised\\Wellington\\mock_transfer\\2006-2007 Project Programme\\2006-07 Project Programme Submission to MoU\\2006-07 Rules Bid_ (🥬) Letter.doc ,2006-07 Rules Bid_ (🥬) Letter.doc,Container,Done,29184,File,doc,2006-03-24T15:45:55,false,294c07b86ad9b460007d1655be2bbf38,1,fmt/40,application/msword,Microsoft Word Document,97-2003
"""

dupe_result: Final[
    str
] = """
"Object Type","Title (DC)","Title (DC)","Access Rights Policy ID (IE)","Archway Unique ID (Object Identifier)","Identifier - Archway Unique Id (DC)","Archway Series Number","Provenance (dcterms)","IE Entity Type","Submission Reason","Event Identifier Type","Event Identifier Value","Event Type","Event Description","Event Date","Event Outcome1","Event Outcome Detail1","Event Outcome Detail Extension1","Event Outcome2","Event Outcome Detail2","Event Outcome Detail Extension2","Event Outcome3","Event Outcome Detail3","Event Outcome Detail Extension3","Revision Number","Usage Type","Representation Code","Preservation Type","Digital Original","File Original Path","File Original Name","File Label","MD5","File Modification Date (General File Characteristics)","File Creation Date (General File Characteristics)"
"SIP","Duplicates Ingest","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""
"IE","","2006-07 Project Programme – MoU invitation to submit","1916130","R25437983","R25437983","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","♙♘♗♖♕♔♚♛♜♝♞♟ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū ♭ ♮ ♯","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Project Programme/","2006-07 Project Programme – MoU invitation to submit.pdf","","294c07b86ad9b460007d1655be2bbf38","2006-02-13T10:45:40",""
"IE","","2006-07 Rules Bid_ (🥬) Letter","1916130","R25437984","R25437984","26000-1","AAAA","ANZ_BornDigital","DigitalTransfer","","","","","","","","","","","","","","","","","","","","","","","","",""
"REPRESENTATION","","","","","","","","","","","","","","","","","","","","","","","","1","VIEW","","♙♘♗♖♕♔♚♛♜♝♞♟ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū ♭ ♮ ♯","TRUE","","","","","",""
"FILE","","","","","","","","","","","","","","","","","","","","","","","","","","","","","2006-2007 Project Programme/2006-07 Project Programme Submission to MoU/","2006-07 Rules Bid_ (🥬) Letter.doc","","294c07b86ad9b460007d1655be2bbf38","2006-03-24T15:45:55",""
"""


def test_duplicates(tmp_path):
    """Provide a basic test for handling duplicates."""

    tmp_dir = tmp_path / "test_dupe_ingest"
    tmp_dir.mkdir()
    config_file = tmp_dir / "config.cfg"
    schema_file = tmp_dir / "schema.json"
    droid_report = tmp_dir / "droid.csv"
    list_control_file = tmp_dir / "lc.csv"

    config_file.write_text(dupe_config.strip().lstrip(), encoding="utf-8")
    schema_file.write_text(schema.strip().lstrip(), encoding="utf-8")
    droid_report.write_text(dupe_droid_csv.strip().lstrip(), encoding="utf-8")
    list_control_file.write_text(dupe_list_control.strip().lstrip(), encoding="utf-8")

    csvgen = RosettaCSVGenerator(
        droid_report,
        list_control_file,
        schema_file,
        config_file,
        "",
    )
    res = csvgen.export_to_rosetta_csv()
    assert res.strip() == dupe_result.strip()
