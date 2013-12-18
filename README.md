mail_migration
==============

Python functions to help when migrating email accounts (requires Apple's Mail.app).

Do you ever migrate email addresses, and you want to take all your messages with you?
If you're like me, you can do most of it with Apple Mail.
Create a new account, create same-named folders, and then folder-by-folder
select all messages and copy (option-drag) them to the new account.
But sometimes, partway through copying a folder full of thousands of messages,
Mail halts with an error or crashes.

The functions in this python script can take over from a partially completed migration,
copying or moving messages from one folder to another without creating duplicates.
They can do basic rate limiting, too.

The script is Python 2.x and depends on the `appscript` AppleEvents bridge.
You can install `appscript` with `easy_install` or `pip`:

    sudo pip-2.7 install appscript

To use it:

    import mail_migration
    
    ## NOTE: mail_migration operates in dry-run mode until you set harmful to True:
    # mail_migration.harmful = True
    
    mail_migration.duplicate_mailbox( ('slackworks', 'travel'), ('gmail', 'travel') )
    
    ## or
    
    mail_migration.duplicate_mailbox( ('ghostinthekell@gmail', u'[Gmail]/All Mail'), ('respectable@gmail', u'[Gmail]/All Mail' ) )
    
    ## To do rate limiting, which can prevent server-imposed hangs, you can do
    import time
    mail_migration.duplicate_mailbox( ('ghostinthekell@gmail', u'[Gmail]/All Mail'), ('respectable@gmail', u'[Gmail]/All Mail' ), limit = 8, action = lambda: time.sleep(3) )

If you want to find out what your accounts and folders are called, use `appscript` directly:
    
    import appscript
    from pprint import pprint
    
    Mail = appscript.app('Mail')
    
    pprint( Mail.accounts.get() )
    
    pprint( Mail.accounts['slackworks'].mailboxes.get() )
    pprint( Mail.accounts['gmail'].mailboxes.get() )

---

## License

I, the author, dedicate this work to the Public Domain.
http://creativecommons.org/publicdomain/zero/1.0/

This software is provided "as is", without warranty of any kind, express or
implied.
