import xml.etree.ElementTree as ET
import os
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def headerAdder(headerobj, headeritem, itemcounter):
    for ic in range(0, itemcounter):
        stric = ''
        if ic in range (0,10):
            stric = "0" + str(ic)
        else:
            stric = str(ic)
        headerobj.append(headeritem+stric)
    return headerobj

def rowObjectAdder(rowobj, rowitem, itemcounter, currobj):
    for ic in range(0, itemcounter):
        try:
            stric=""
            if ic in range(0, 10):
                stric = "0"+ str(ic)
            else:
                stric = str(ic)
            rowobj[rowitem + stric] = currobj[ic].encode('utf-8')
        except IndexError:
            rowobj[rowitem + stric] = ''

    return rowobj

Issues = []
IssueCounter = 0
IssueOrganizationCounter = []
IssueVersionCounter = []
IssueFixVersionCounter = []
IssueComponentCounter = []
IssueCommentsCounter = []
IssueAttachmentsCounter = []
IssueSubtaskCounter = []
IssueLink_To_Counter = []
IssueduplicatesCounter = []
Issueis_Linked_ByCounter = []
Issueis_duplicated_byCounter = []

project = input("1 = Project1, 2 = Project2, 3 = Project3. 4 = Project4. Enter a number: ")

if project == 1:
    xmlfile = 'Project1.xml'
    outputtype = "Project1"

if project == 2:
    xmlfile = 'Project2.xml'
    outputtype = "Project2"

if project == 3:
    xmlfile = 'Project2.xml'
    outputtype = 'Project3'

if project == 4:
    xmlfile = 'Project4.xml'
    outputtype = 'Project4'

with open(xmlfile, 'r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()

tasksWithParents = {}

#Get the sub-tasks
for channel in root:
    for item in channel:
        if item.tag == 'item':
            for subitem in item:
                currentParent = ''
                if subitem.tag == 'key':
                    currentParent = subitem.text

                if subitem.tag == 'subtasks':
                    for subtask in subitem:
                        tasksWithParents[subtask.text] = currentParent

#Do the rest
for channel in root:

    for item in channel:
        if item.tag == 'item':
            IssueCounter += 1
            currIssue = {}
            OrganizationCounter = 0
            VersionCounter = 0
            FixVersionCounter = 0
            ComponentCounter = 0
            CommentsCounter = 0
            AttachmentsCounter = 0

            Link_To_Counter = 0
            duplicatesCounter = 0
            is_Linked_ByCounter = 0
            is_duplicated_byCounter = 0

            ParentCounter = 0

            Organizations = []
            LinkedIssues = []
            Versions = []
            fixVersions = []
            Components = []
            Comments = []
            Attachments = []

            Linked_ToList = []
            duplicatesList = []
            is_Linked_ByList = []
            is_duplicated_byList = []

            currKey = ''

            for subitem in item:
                if subitem.tag == 'key':
                    currIssue['key'] = subitem.text
                    currKey = subitem.text
                if subitem.tag == 'summary':
                    currIssue['summary'] = subitem.text.encode('utf8')
                if subitem.tag == 'description':
                    desctext = subitem.text
                    if desctext is not None:
                        currIssue['description'] = desctext.encode('utf8').replace('<br/>', '')
                    else:
                        currIssue['description'] = ''
                if subitem.tag == 'type':
                    currIssue['type'] = subitem.text
                if subitem.tag == 'priority':
                    currIssue['priority'] = subitem.text
                if subitem.tag == 'status':
                    currIssue['status'] = subitem.text
                if subitem.tag == 'resolution':
                    currIssue['resolution'] = subitem.text
                if subitem.tag == 'assignee':
                    currIssue['assignee'] = subitem.get('username')
                if subitem.tag == 'reporter':
                    currIssue['reporter'] = subitem.get('username')
                if subitem.tag == 'created':
                    currIssue['created'] = subitem.text
                if subitem.tag == 'updated':
                    currIssue['updated'] = subitem.text

                if subitem.tag == 'parent':
                    ParentCounter += 1
                    parent = subitem.text
                    issueID = ''

                if ParentCounter < 1:
                    issueID = currKey
                    parent = ''

                currIssue['issueID'] = issueID
                currIssue['parent'] = parent

                workcategory = ''
                if subitem.tag == 'customfields':
                    for customfield0 in subitem:
                        if customfield0.tag == 'customfield':
                            customfieldtype = customfield0.find('customfieldname').text
                            if customfieldtype == 'Work Category':
                                for customfield1 in customfield0:
                                    if customfield1.tag == 'customfieldvalues':
                                        for customfieldvalue in customfield1:
                                            if customfieldvalue.tag == 'customfieldvalue':
                                                workcategory = customfieldvalue.text
                currIssue['workcategory'] = workcategory

                usage = ''
                if subitem.tag == 'customfields':
                    for customfield0 in subitem:
                        if customfield0.tag == 'customfield':
                            customfieldtype = customfield0.find('customfieldname').text
                            if customfieldtype == 'Usage':
                                for customfield1 in customfield0:
                                    if customfield1.tag == 'customfieldvalues':
                                        for customfieldvalue in customfield1:
                                            if customfieldvalue.tag == 'customfieldvalue':
                                                usage = customfieldvalue.text
                currIssue['usage'] = usage

                severity = ''
                if subitem.tag == 'customfields':
                    for customfield0 in subitem:
                        if customfield0.tag == 'customfield':
                            customfieldtype = customfield0.find('customfieldname').text
                            if customfieldtype == 'Severity':
                                for customfield1 in customfield0:
                                    if customfield1.tag == 'customfieldvalues':
                                        for customfieldvalue in customfield1:
                                            if customfieldvalue.tag == 'customfieldvalue':
                                                severity = customfieldvalue.text
                currIssue['severity'] = severity


                if subitem.tag == 'customfields':
                    for customfield0 in subitem:
                        if customfield0.tag == 'customfield':
                            customfieldtype = customfield0.find('customfieldname').text
                            if customfieldtype == 'Organization(s)':
                                for customfield1 in customfield0:
                                    if customfield1.tag == 'customfieldvalues':
                                        for customfieldvalue in customfield1:
                                            if customfieldvalue.tag == 'customfieldvalue':
                                                OrganizationCounter += 1
                                                Organizations.append(customfieldvalue.text)
                Linked_To = ''
                duplicates = ''
                is_Linked_By = ''
                is_duplicated_by = ''

                if subitem.tag == 'issuelinks':
                    for issuelinktype in subitem:
                        if issuelinktype.tag == 'issuelinktype':
                            for outwardlinks in issuelinktype:
                                if outwardlinks.tag == 'outwardlinks':
                                    #get the description
                                    LinkType = outwardlinks.get('description')
                                    #Linked To
                                    #duplicates
                                    for issuelink in outwardlinks:
                                        if issuelink.tag == 'issuelink':
                                            for issuekey in issuelink:
                                                if (issuekey.tag == 'issuekey'):
                                                    if LinkType == 'Linked To':
                                                        Linked_To = issuekey.text
                                                        Linked_ToList.append(Linked_To)
                                                        Link_To_Counter += 1
                                                    if LinkType == 'duplicates':
                                                        duplicates = issuekey.text
                                                        duplicatesList.append(duplicates)
                                                        duplicatesCounter += 1
                            for inwardlinks in issuelinktype:
                                if inwardlinks.tag == 'inwardlinks':
                                    # get the description
                                    LinkType = inwardlinks.get('description')
                                    #is Linked By
                                    #is duplicated by
                                    for issuelink in inwardlinks:
                                        if issuelink.tag == 'issuelink':
                                            for issuekey in issuelink:
                                                if (issuekey.tag == 'issuekey'):
                                                    if LinkType == 'is Linked By':
                                                        is_Linked_By = issuekey.text
                                                        is_Linked_ByList.append(is_Linked_By)
                                                        is_Linked_ByCounter +=1
                                                    if LinkType == 'is duplicated by':
                                                        is_duplicated_by = issuekey.text
                                                        is_duplicated_byList.append(is_duplicated_by)
                                                        is_duplicated_byCounter +=1

                if subitem.tag == 'version':
                    Versions.append(subitem.text)
                    VersionCounter += 1
                if subitem.tag == 'fixVersion':
                    fixVersions.append(subitem.text)
                    FixVersionCounter += 1
                if subitem.tag == 'component':
                    ComponentCounter += 1
                    Components.append(subitem.text)
                if subitem.tag == 'comments':
                    for comments in subitem:
                        comments.text = comments.text.replace('<br/>', '')
                        CommentsCounter += 1
                        commenttext = comments.get('created') + ';' + comments.get('author') + ';' + comments.text
                        if commenttext is not None:
                            commenttext = commenttext
                            Comments.append(commenttext)
                        else:
                            commenttext = ''
                            Comments.append(commenttext)
                if subitem.tag == 'attachments':
                    for attachments in subitem:
                        AttachmentsCounter += 1
                        attachmenttext = attachments.get('name')
                        if attachmenttext is not None:
                            attachmenttext = attachmenttext.encode('utf8')
                            attachmenttext = attachmenttext.replace(' ','+')
                            Attachments.append("file://"+currIssue['key']+"/"+attachmenttext)
                        else:
                            attachmenttext = ''
                            Comments.append(attachmenttext)

            currIssue['organizations'] = Organizations
            currIssue['linkedissues'] = LinkedIssues
            currIssue['affectsversions'] = Versions
            currIssue['fixversions'] = fixVersions
            currIssue['components'] = Components
            currIssue['comments'] = Comments
            currIssue['attachments'] = Attachments
            currIssue['Linked_To'] = Linked_ToList
            currIssue['duplicates'] = duplicatesList
            currIssue['is_Linked_by'] = is_Linked_ByList
            currIssue['is_duplicated_by'] = is_duplicated_byList

            IssueOrganizationCounter.append(OrganizationCounter)
            IssueVersionCounter.append(VersionCounter)
            IssueFixVersionCounter.append(FixVersionCounter)
            IssueComponentCounter.append(ComponentCounter)
            IssueCommentsCounter.append(CommentsCounter)
            IssueAttachmentsCounter.append(AttachmentsCounter)
            IssueLink_To_Counter.append(Link_To_Counter)
            IssueduplicatesCounter.append(duplicatesCounter)
            Issueis_Linked_ByCounter.append(is_Linked_ByCounter)
            Issueis_duplicated_byCounter.append(is_duplicated_byCounter)

            Issues.append(currIssue)

TotalIssues = IssueCounter
MaxOrganizations = max(IssueOrganizationCounter)
MaxAffectsVersion = max(IssueVersionCounter)
MaxFixVersion = max(IssueFixVersionCounter)
MaxComponent = max(IssueComponentCounter)
MaxComments = max(IssueCommentsCounter)
MaxAttachments = max(IssueAttachmentsCounter)

MaxLink_To = max(IssueLink_To_Counter)
Maxduplicates = max(IssueduplicatesCounter)
Maxis_Linked_By = max(Issueis_Linked_ByCounter)
Maxis_duplicated_by = max(Issueis_duplicated_byCounter)

print "Total Issues: " + str(TotalIssues)
print "Max Organizations: " +str(MaxOrganizations)
print "Max Affects Version: " + str(MaxAffectsVersion)
print "Max Fix Versions: " + str(MaxFixVersion)
print "Max Components: " + str(MaxComponent)
print "Max Comments: " + str(MaxComments)
print "Max Attachments: " + str(MaxAttachments)
print "Max Link To: " + str(MaxLink_To)
print "Max Duplicates: " + str(Maxduplicates)
print "Max Linked By: " + str(Maxis_Linked_By)
print "Max Duplicated By: " + str(Maxis_duplicated_by)


headerrow = []
#headerrow.append('Project Name')
#headerrow.append('Project Key')
headerrow.append('Summary')
headerrow.append('Issue Key')
headerrow.append('Description')
headerrow.append('Issue Type')
headerrow.append('Priority')
headerrow.append('Status')
headerrow.append('Resolution')
headerrow.append('Assignee')
headerrow.append('Reporter')
headerrow.append('Created')
headerrow.append('Modified')
headerrow.append('workcategory')
headerrow.append('usage')
headerrow.append('severity')
headerrow.append('issueID')
headerrow.append('parent')

headerrow = headerAdder(headerrow,'Linked_To', MaxLink_To)
headerrow = headerAdder(headerrow,'duplicates', Maxduplicates)
headerrow = headerAdder(headerrow,'is_Linked_by', Maxis_Linked_By)
headerrow = headerAdder(headerrow,'is_duplicated_by', Maxis_duplicated_by)

headerrow = headerAdder(headerrow, 'organizations', MaxOrganizations)
headerrow = headerAdder(headerrow, 'affectsversions', MaxAffectsVersion)
headerrow = headerAdder(headerrow, 'fixversions', MaxFixVersion)
headerrow = headerAdder(headerrow, 'components', MaxComponent)
headerrow = headerAdder(headerrow, 'comments', MaxComments)
headerrow = headerAdder(headerrow, 'attachments', MaxAttachments)

print headerrow

dir_path = os.path.dirname(os.path.realpath(__file__))

print dir_path

full_path = dir_path + "/"+outputtype+"_csv.csv"

print full_path

try:
    os.remove(full_path)
except OSError:
    pass

with open(full_path, 'wb',) as csvfile:
    writer = csv.DictWriter(csvfile, headerrow, delimiter = ',', quoting=csv.QUOTE_ALL)
    writer.writeheader()

    ThrottleIssuesCounter = 0
    for Issue in Issues:
        currRow = {}
        currRow['Issue Key'] = Issue['key']
        currRow['Summary'] = Issue['summary']
        currRow['Description'] = Issue['description']
        currRow['Issue Type'] = Issue['type']
        currRow['Priority'] = Issue['priority']
        currRow['Status'] = Issue['status']
        currRow['Resolution'] = Issue['resolution']
        currRow['Assignee'] = Issue['assignee']
        currRow['Reporter'] = Issue['reporter']
        currRow['Created'] = Issue['created']
        currRow['Modified'] = Issue['updated']
        currRow['workcategory'] = Issue['workcategory']
        currRow['usage'] = Issue['usage']
        currRow['severity'] = Issue['severity']
        currRow['issueID'] = Issue['issueID']
        currRow['parent'] = Issue['parent']

        currRow = rowObjectAdder(currRow, 'Linked_To', MaxLink_To, Issue['Linked_To'])
        currRow = rowObjectAdder(currRow, 'duplicates', Maxduplicates, Issue['duplicates'])
        currRow = rowObjectAdder(currRow, 'is_Linked_by', Maxis_Linked_By, Issue['is_Linked_by'])
        currRow = rowObjectAdder(currRow, 'is_duplicated_by', Maxis_duplicated_by, Issue['is_duplicated_by'])

        currRow = rowObjectAdder(currRow, 'organizations', MaxOrganizations, Issue['organizations'])
        currRow = rowObjectAdder(currRow, 'affectsversions', MaxAffectsVersion, Issue['affectsversions'])
        currRow = rowObjectAdder(currRow, 'fixversions', MaxFixVersion, Issue['fixversions'])
        currRow = rowObjectAdder(currRow, 'components', MaxComponent, Issue['components'])
        currRow = rowObjectAdder(currRow, 'comments', MaxComments, Issue['comments'])
        currRow = rowObjectAdder(currRow, 'attachments', MaxAttachments, Issue['attachments'])

        writer.writerow(currRow)
        ThrottleIssuesCounter=ThrottleIssuesCounter+1

# Comment Order: https://confluence.atlassian.com/jirakb/sort-comments-added-to-jira-issue-via-csv-import-587302255.html
# Attachments: https://confluence.atlassian.com/jira061/jira-administrators-faq/usage-faq/how-to-import-attachment-using-csv