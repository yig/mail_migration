'''
###
### License:
###
Author: Yotam Gingold <yotam@yotamgingold.com>

Any copyright is dedicated to the Public Domain.
http://creativecommons.org/publicdomain/zero/1.0/

This software is provided "as is", without warranty of any kind, express or
implied.


###
### Example usage:
###

import mail_migration

## NOTE: mail_migration operates in dry-run mode until you set harmful to True:
# mail_migration.harmful = True

mail_migration.duplicate_mailbox( ('slackworks', 'travel'), ('gmail', 'travel') )

## or

mail_migration.duplicate_mailbox( ('ghostinthekell@gmail', u'[Gmail]/All Mail'), ('respectable@gmail', u'[Gmail]/All Mail' ) )

## To do rate limiting, which can prevent server-imposed hangs, you can do
import time
mail_migration.duplicate_mailbox( ('ghostinthekell@gmail', u'[Gmail]/All Mail'), ('respectable@gmail', u'[Gmail]/All Mail' ), limit = 8, action = lambda: time.sleep(3) )


###
### If you want to find out what your accounts and folders are called, use `appscript` directly:
###

import appscript
from pprint import pprint

Mail = appscript.app('Mail')

pprint( Mail.accounts.get() )

pprint( Mail.accounts['slackworks'].mailboxes.get() )
pprint( Mail.accounts['gmail'].mailboxes.get() )
'''

import appscript

harmful = False

## Example appscript usage:
#msgs = appscript.app('Mail').accounts[u'slackworks'].mailboxes[u'INBOX/Junk'].messages.get()

def move_mailbox( (src_account, src_mailbox), (dst_account, dst_mailbox), limit = None, action = None ):
    '''
    Moves non-duplicate messages from the mailbox named 'src_mailbox' in account 'src_account'
    to the mailbox 'dst_mailbox' in account 'dst_account'.
    
    After copying 'limit' messages, terminates unless action is not None, in which case
    'action()' is called ever 'limit' messages.
    NOTE: This is useful because Mail may spawn a thread for every message and we have no
          way of knowing when each command is completed, so you can pass e.g.
          limit = 10, action = lambda: time.sleep(3)
    
    Example usage:
    move_mailbox( ('slackworks', 'travel'), ('slackworks@gmail', 'travel') )
    '''
    
    Mail = appscript.app('Mail')
    msgs = Mail.accounts[src_account].mailboxes[src_mailbox].messages.get()
    move_msgs( msgs, (dst_account, dst_mailbox), limit, action )

def move_selection( (dst_account, dst_mailbox), limit = None, action = None ):
    '''
    Moves non-duplicate messages selected in Mail.app
    to the mailbox 'dst_mailbox' in account 'dst_account'.
    
    After copying 'limit' messages, terminates unless action is not None, in which case
    'action()' is called ever 'limit' messages.
    NOTE: This is useful because Mail may spawn a thread for every message and we have no
          way of knowing when each command is completed, so you can pass e.g.
          limit = 10, action = lambda: time.sleep(3)
    
    Example usage:
    move_selection( ('slackworks@gmail', 'travel') )
    '''
    
    Mail = appscript.app('Mail')
    msgs = Mail.selection.get()
    move_msgs( msgs, (dst_account, dst_mailbox), limit, action )

def move_msgs( msgs, (dst_account, dst_mailbox), limit = None, action = None ):
    '''
    Low-level, shared by move_mailbox() and move_selection().
    '''
    
    Mail = appscript.app('Mail')
    
    dst = Mail.accounts[dst_account].mailboxes[dst_mailbox].get()
    dst_msg_ids_list = [ msg.message_id.get() for msg in dst.messages.get() ]
    dst_msg_ids = set( dst_msg_ids_list )
    print 'By the way, %s/%s messages in the destination %s/%s are duplicates' % (len(dst_msg_ids_list) - len(dst_msg_ids), len(dst_msg_ids_list), dst_account, dst_mailbox)
    
    count = 0
    N = len( msgs )
    for i, msg in enumerate( msgs ):
        msg_id = msg.message_id.get()
        if msg_id not in dst_msg_ids:
            if limit is not None and count >= limit:
                if action is None: return
                else: action()
                count = 0
            count += 1
            print 'Moving msg %s to mailbox %s/%s' % (msg_id, dst_account, dst_mailbox)
            try:
                if harmful: msg.mailbox.set( dst )
            except:
                print 'FAILED:', msg
        else:
            print 'Skipping msg %s since it\'s already there' % (msg_id,)
        if (i % 10) == 0: print '%s/%s complete' % (i+1, N)

def duplicate_mailbox( (src_account, src_mailbox), (dst_account, dst_mailbox), limit = None, action = None ):
    '''
    Copies non-duplicate messages from the mailbox named 'src_mailbox' in account 'src_account'
    to the mailbox 'dst_mailbox' in account 'dst_account'.
    
    After copying 'limit' messages, terminates unless action is not None, in which case
    'action()' is called ever 'limit' messages.
    NOTE: This is useful because Mail may spawn a thread for every message and we have no
          way of knowing when each command is completed, so you can pass e.g.
          limit = 10, action = lambda: time.sleep(3)
    
    Example usage:
    duplicate_mailbox( ('slackworks', 'travel'), ('slackworks@gmail', 'travel') )
    
    NOTE: 
    '''
    
    Mail = appscript.app('Mail')
    msgs = Mail.accounts[src_account].mailboxes[src_mailbox].messages.get()
    duplicate_msgs( msgs, (dst_account, dst_mailbox), limit, action )

def duplicate_selection( (dst_account, dst_mailbox), limit = None, action = None ):
    '''
    Copies non-duplicate messages selected in Mail.app
    to the mailbox 'dst_mailbox' in account 'dst_account'.
    
    After copying 'limit' messages, terminates unless action is not None, in which case
    'action()' is called ever 'limit' messages.
    NOTE: This is useful because Mail may spawn a thread for every message and we have no
          way of knowing when each command is completed, so you can pass e.g.
          limit = 10, action = lambda: time.sleep(3)
    
    Example usage:
    duplicate_selection( ('slackworks@gmail', 'travel') )
    '''
    
    Mail = appscript.app('Mail')
    msgs = Mail.selection.get()
    duplicate_msgs( msgs, (dst_account, dst_mailbox), limit, action )

def duplicate_msgs( msgs, (dst_account, dst_mailbox), limit = None, action = None ):
    '''
    Low-level, shared by duplicate_mailbox() and duplicate_selection().
    '''
    
    Mail = appscript.app('Mail')
    
    dst = Mail.accounts[dst_account].mailboxes[dst_mailbox].get()
    dst_msg_ids_list = [ msg.message_id.get() for msg in dst.messages.get() ]
    dst_msg_ids = set( dst_msg_ids_list )
    print 'By the way, %s/%s messages in the destination %s/%s are duplicates' % (len(dst_msg_ids_list) - len(dst_msg_ids), len(dst_msg_ids_list), dst_account, dst_mailbox)
    
    count = 0
    N = len( msgs )
    for i, msg in enumerate( msgs ):
        msg_id = msg.message_id.get()
        if msg_id not in dst_msg_ids:
            if limit is not None and count >= limit:
                if action is None: return
                else: action()
                count = 0
            count += 1
            print 'Copying msg %s to mailbox %s/%s' % (msg_id, dst_account, dst_mailbox)
            try:
                if harmful: msg.duplicate( to = dst )
            except:
                print 'FAILED:', msg
        else:
            print 'Skipping msg %s since it\'s already there' % (msg_id,)
        if (i % 10) == 0: print '%s/%s complete' % (i+1, N)
