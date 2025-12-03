# The Fancy Contact Page

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

The fancy contact page is now ubiquitous in any Salesforce Demo. There are so many variations of this it’s getting to be a joke now.

You know what happens, you client or boss sees that demo and says why doesn’t our contact page look like this? Why indeed? Go ask you AE and say “can you sell me the things that will make my contact page look like this”. No, they will try to sell you Data Cloud and everything under the sun and still your page will NOT look like that.

The Perfect Contact Page

To me, this is still the perfect contact page:

Open image-20231029-034825.png

Highlights Panel

Buttons on the right

Only the buttons needed

Dynamic Actions

Large Column with detail layout

Detail first

Related Second

Narrow column with things to focus on

Salesforce Indicators at the top to show what needs done next or what is important

Duplicate checking (whether standard Salesforce duplicates that are far from adequate, or your duplicate manager of choice.

Chatter First

Chatter is so important!

Activities Second

Detail page structured:

I STILL subscribe to these rules

Usability: Fields and Page Layouts

Descriptive fields on the left

Action fields on the right

Good sections structure

Address down the bottom of the page

Things I may add:

Formulas to the Highlights Panel - eg

City State Country

More useful tools in the Utility Bar

A Related List of the next things to look at - only contextual - eg if there are Open Cases or Open Opportunities, I may display them at the top of the detail page for the Sales or Support team only.

Related List Quick Links component if there are a lot of related lists.

Dynamic Related Lists

A good Files component on a separate tab - see

Files, Content, Attachments, Documents etc.

Report Chart Component and Record Reports on a separate tab

I may go to Dynamic Forms if needed (Dynamic Actions are already done)

Dynamic Forms and Dynamic Actions

Some Example Demo Pages

Expand to see some example demo pages

See one on the

The Magical Demo Record Page page… but that doesn’t have the Contact panel, which is the key thing we are talking about here.

This one is one of the simpler layouts that is within reach of us maybe re-creating something similar

Open image-20231029-042333.png

Do I really really need 1/3 of the page taken up with key information, and another 3rd of the page taken up with history?

Let’s delve into some of the issues with this layout:

No Activity buttons - anywhere

No Enhanced List Views

The first and most visible action to take is to create a New Opportunity - this may be good for business, but it’s not putting the customer first, as they already have an open Opportunity

Details Tab second

It’s not obvious for me what to do next

How do I quickly update the email address?

How do I quickly make a note about what my plans are next for working with Lauren?

What works for me

Lifetime Value - but what about her value in relation to other customers

Highly Engaged - but is the gauge actually telling me anything

I like the other activities such as Email Opened, Website Visit

What is not working for me

Customer ID being the most important field

Powered by - no one would have that there other than in a demo

Full Address - I don’t need to take up space in my highlights panel

I can’t click on the email or phone number to quickly do anything

I like the photo but I don’t have photos of all my clients so it’s a big blank space otherwise.

Overall, a layout like this may work if you are fully focused on things that have happened in the past. But if you have a lot of detail fields that you need to capture about a Contact, or any other record, a page layout like this is just a waste of space. No matter what these demo people are trying to show you, the act of updating a record is still what a majority of users do a majority of the time when interacting with Salesforce. This is also why I don’t understand how and why people want to surface Salesforce records in Slack.

Let’s think of some fields you may need on the Contact:

All the key NPSP / NPC fields for donations and latest and largest gift value etc

For a University, key fields about Alumni Status, Study Area, Faculty, Student Number, Majors, Alma Mata, Fraternity (for the US folk).

For Events, the full name with salutations and honors and a Partner Name for invitations (Hopefully a formula field from the other person in the Household)

For Marketing, the topics of interest that you are targeting them for

For Contracts, middle name and suffix fields, local language name fields, date of birth

For Office Management contacts, the assistant details (however I think they should be a related contact)

For Families, the parents (hopefully automated from a Household record)

For Accounts teams, the ID in the billing system, the highest level of discount authorised (or that could be on the Account usually)

And we could go on and on…

Do all these fields need to be on the side panel? No, probably not, but they are key fields that need to be there for staff to see and edit, quickly and easily - without having to click elsewhere.

In a perfect world we would design our page layouts for only the Marketing team to see Marketing information, but in small businesses everyone usually needs to know everything, and marketing information may be relevant to the Accounts team also.

Sidebar - check this REAL layout out

Highlights Panel

The Highlights Panel, based on the Compact Layout is soooo limiting.

No different layout for different record types

No conditionally visible fields

Only 6 fields

BUT, it has some great features:

Phone and Email fields stack under a caret

Email shows bounced flag

Hierarchy button

Change Owner button

The Object Icon for quick recognition that you are on the right record

You can show it as collapsed by default (I don’t like collapsed layout though).

For me, Highlights Panels are critical, and they should be the consistent throughout the whole of Salesforce. I do not want to jump around to different looking pages, unless there is a really good reason for it. If I have very deep nested records (eg Parent > Child > Child > Child) I will make a breadcrumbs style formula field as the second field, with URLs so that they can jump back to any level quickly.

It is annoying that any non key object doesn’t have a highlights panel created out of the box and you have to create them for every object. Maybe that is what Generative AI actions can help us to do.

Highlights Panel can go on the left hand panel BUT…

The buttons are all smooshed up

That may be more doable when we have the Dynamic Actions Button Bar or whatever they are going to call it after it comes out of Pilot (but it’s been there for a few years now).

The buttons are in the way of the data

It is not natural to have buttons on the left hand side (if you read from left to right - buttons to the right denote next / move forward / do something now).

What do you put below?

Anything looks weird, even Salesforce Indicators

The fields look more duplicated when they are in the highlights panel and on the page

You can still only have 6 fields

Open image-20231029-052509.png

Weirdly, this layout uses Pinned Header, even though we are not using it. see

The Magical Demo Record Page. It’s the only standard layout with the wide middle column.

Can we Build this ourselves

No, not without a custom LWC

Aha, someone in the community DID build this with an LWC! See Mykhalio Vdovychenko’s Post

And Infallible Techie’s Post.

Open image-20231029-062602.png

Look, I worked on this for 2 hours and still it is exceptionally ugly, and non functional:

I tried 4 different image Appexchange apps - this was the best I could get an image to display. So much real estate for very little benefit. The tiny File preview could be enough.

I did not try the Picture Uploader app that Mykhalio tried, becuase it has Vertical Nav in the Appexchange pictures, and now that I have tried it, it uses Visualforce Components and Attachments. YUK!

I tried the Labs Highlights Panel app to separate out the highlights fields and buttons.

The buttons on the left are not good - as noted above.

I like the indicators to be on the right still.

I still want my details pane first.

So what’s the answer

I don’t know… yet… I have tried other page layouts and I still can’t go past my original layout.

As part of Salesforce Indicators, we are planning to do a Panel Component that will take the icons and show them as text, like in the highlights panel, with the following features:

Show different values based on different Record Types

Show different fields based on record Statuses

Show different labels to the field labels

Show coloured pills and badges and even icons mixed in with the field values.

Display more than 6-10 fields

Profile (or Custom Permission) based (worst case, Lightning Record Pages allows conditional visibility and you can install multiple Highlights panels)

Display fields from parent record(s)

Support text area (and multi-select picklists)

Conditional visibility of fields (only show when a condition is met or not met - which is what Indicators does)

Conditional formatting of fields to draw attention to them

Should we add an image field as an option?

Should we add a coloured background as an option? Or a header?

Should we make the panel be available both vertically and horizontally?

I think we could do something more similar to this one (with a photo if they have a photo URL in a specific field).

Open image-20231029-073213.png

However, at this stage, there is no huge value in building something, as there was a Dynamic Highlights Panel in the September 2023 Prioritization round, and we don’t know what that will be yet. And I think we should wait until there is a clear indication if they are going to give us the floating button bar too.

What are your thoughts?