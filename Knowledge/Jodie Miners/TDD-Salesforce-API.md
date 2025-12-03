# Salesforce API

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

Overview

Multiple API's

2 you need to know about - REST and SOAP

See Rest API Vs SOAP API in Salesforce - Salesforce Stack Exchange for some links to some in depth documentation.

REST

Uses JSON

Readable, Name Value Pairs

Good for querying one record at time or retrieving a small subset of records.

Can't have a transaction.

Developers don't need to know the full specification of the API, they can query it as they go.

Eg Accounts/Contacts/Fields to see what fields are accessible.

Uses nouns to find things.

Uses verbs such as GET (query), POST (create) to do stuff or PATCH (to update a record).

Apex REST

Can do multiple things on the one POST - eg Update the Account and Contact.

Almost a transaction.

Be careful with the security, the salesforce developer will have to write the security explicitly.

Now getting used much more because of the rise in mobile apps for Salesforce.

SOAP

Uses XML

Requires the WSDL file to be downloaded to find out what the methods are that can be called.

Still widely used in the Salesforce world.

Mainly used for enterprise level access.

Features

there are a few scenarios that are not supported OOTB in Force.com – complex data queries (i.e. joins) via the API, custom logic or rules, and anonymous access.

Others

Metadata API

using tools like Mavens Mate (See MavensMate and Git for Non Developers).

Tooling API

Chatter API

A lightweight REST API to just use Chatter.

Streaming API

Replaces batch jobs.

Data is pushed to the API whenever it changes.

Like push notifications on your phone.

Javascript Remoting

New Javascript thingy???

Developers will have a definite opinion on which ones they will use.

Know enough to question them

Security

Token

Hard Coded

Insecure

Just about every dev app will use them, and your Dev has admin access.

Every time you change passwords, needs to be reset.

Annoying

If they are used on your website, and hard coded, what is the security of your website like?

Check what your app is using. Try to get your devs to change to OAuth.

See also Apps using Token Authentication - I'm compiling a list of apps that I know use Tokens.

OAuth

User to User only is best.

Don't use for anonymous access if possible.

What is saved

No granularity

What they can see.

Can be revoked at any time.

Can be revoked by admins or users.

A re-usable token is stored.

Ways apps can access your Salesforce data

Granted explicitly by logging in with a token

Granted explicitly by a user doing OAUTH connection

Installing an app that uses a third party service.

Passing data via URLs

Be very careful of passing your data from your Salesforce org to third party services via URLs.

Example http://www.webmerge.me/blog/create-pdf-contracts-agreements-from-salesforce (this is not the only one, may apps do it, including Form Assembly.

Ensure both ends have SSL

Ensure it does not query Salesforce in a way that can be guessed or manipulated (eg pre-filling with AccountID=1234 and someone changes the URL to 1235 and gets someone else's details.

This can be overcome with a token (see the way Form Assembly enterprise edition does it).

Denying

Turn off the API Enabled permission for users that don't need it.

However, In practice this can be quite limiting because many many apps use the API.

Block individual apps. See this great post by Cloud Sherpas on monitoring and blocking Apps Managing External Apps with Connected Apps - Cloud Sherpas

Monitoring

As a SF Admin you need to monitor all apps that have a connection to your Org.

Setup > Manage Apps > Connected Apps OAuth Usage.

Your Name > Personal > Connections shows the apps that each user is connected to.

But that is not the full story - there may be apps that are connected via token.

Be aware of any apps that are connected via a token.

If necessary:

Revoke connections

Reset user passwords, that will reset the tokens also.

The security token is valid until a user resets their security token, changes their password, or has their password reset.

Articles

Articles about the Salesforce API.

Article Title	Link

Start building your own REST API in Salesforce using Apex	www.oyecode.com/2014/08/start…

How to use the new Salesforce REST API from PHP	petewarden.com/2010/10/29/how…

Creating Anonymous Apex REST APIs with Force.com - Wade Wegner	 www.wadewegner.com/2013/03/cr…

Rest API Vs SOAP API in Salesforce - Salesforce Stack Exchange	 salesforce.stackexchange.com/…

Creating Anonymous Apex REST APIs with Force.com	 www.wadewegner.com/2013/03/cr…

Building apps with the Salesforce API | Appery.io Docs	 docs.appery.io/documentation/…

Managing External Apps with Connected Apps - Cloud Sherpas	 www.cloudsherpas.com/partner-…

Digging Deeper into OAuth 2.0 on Force.com - developer.force.com	 wiki.developerforce.com/page/…

WordPress › Gravity Forms Salesforce Add-on « WordPress Plugins	 wordpress.org/plugins/gravity…

Salesforce.com Workbench Overview	 jessealtman.com/2013/09/sales…