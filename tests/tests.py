# -*- coding: utf-8 -*-
r"""
>>> from tagging.models import Tag, TaggedItem
>>> from tagging.tests.models import Article, Link, Parrot

###########
# Tagging #
###########

# Basic tagging ###############################################################

>>> dead = Parrot.objects.create(state='dead')
>>> Tag.objects.update_tags(dead, 'foo bar ter')
>>> Tag.objects.get_for_object(dead)
[<Tag: bar>, <Tag: foo>, <Tag: ter>]
>>> Tag.objects.update_tags(dead, 'foo bar baz')
>>> Tag.objects.get_for_object(dead)
[<Tag: bar>, <Tag: baz>, <Tag: foo>]

# Note that doctest in Python 2.4 (and maybe 2.5?) doesn't support non-ascii
# characters in output, so we're displaying the repr() here.
>>> Tag.objects.update_tags(dead, 'ŠĐĆŽćžšđ')
>>> repr(Tag.objects.get_for_object(dead))
'[<Tag: \xc5\xa0\xc4\x90\xc4\x86\xc5\xbd\xc4\x87\xc5\xbe\xc5\xa1\xc4\x91>]'

>>> Tag.objects.update_tags(dead, None)
>>> Tag.objects.get_for_object(dead)
[]

# Retrieving tags by Model ####################################################

>>> Tag.objects.usage_for_model(Parrot)
[]
>>> Tag.objects.update_tags(Parrot.objects.create(state='pining for the fjords'), 'foo bar')
>>> Tag.objects.update_tags(Parrot.objects.create(state='passed on'), 'bar baz ter')
>>> Tag.objects.update_tags(Parrot.objects.create(state='no more'), 'foo ter')
>>> Tag.objects.update_tags(Parrot.objects.create(state='late'), 'bar ter')
>>> [(tag.name, tag.count) for tag in Tag.objects.usage_for_model(Parrot, counts=True)]
[('bar', 3), ('baz', 1), ('foo', 2), ('ter', 3)]

# Retrieving tagged objects by Model ##########################################

>>> foo = Tag.objects.get(name='foo')
>>> bar = Tag.objects.get(name='bar')
>>> baz = Tag.objects.get(name='baz')
>>> ter = Tag.objects.get(name='ter')
>>> TaggedItem.objects.get_by_model(Parrot, foo)
[<Parrot: no more>, <Parrot: pining for the fjords>]
>>> TaggedItem.objects.get_by_model(Parrot, bar)
[<Parrot: late>, <Parrot: passed on>, <Parrot: pining for the fjords>]

# Intersections are supported
>>> TaggedItem.objects.get_by_model(Parrot, [foo, baz])
[]
>>> TaggedItem.objects.get_by_model(Parrot, [foo, bar])
[<Parrot: pining for the fjords>]
>>> TaggedItem.objects.get_by_model(Parrot, [bar, ter])
[<Parrot: late>, <Parrot: passed on>]

# You can also pass a Tag QuerySet
>>> TaggedItem.objects.get_by_model(Parrot, Tag.objects.filter(name__in=['foo', 'baz']))
[]
>>> TaggedItem.objects.get_by_model(Parrot, Tag.objects.filter(name__in=['foo', 'bar']))
[<Parrot: pining for the fjords>]
>>> TaggedItem.objects.get_by_model(Parrot, Tag.objects.filter(name__in=['bar', 'ter']))
[<Parrot: late>, <Parrot: passed on>]

# Retrieving related objects by Model #########################################

# Related instances of the same Model
>>> l1 = Link.objects.create(name='link 1')
>>> Tag.objects.update_tags(l1, 'tag1 tag2 tag3 tag4 tag5')
>>> l2 = Link.objects.create(name='link 2')
>>> Tag.objects.update_tags(l2, 'tag1 tag2 tag3')
>>> l3 = Link.objects.create(name='link 3')
>>> Tag.objects.update_tags(l3, 'tag1')
>>> l4 = Link.objects.create(name='link 4')
>>> TaggedItem.objects.get_related(l1, Link)
[<Link: link 2>, <Link: link 3>]
>>> TaggedItem.objects.get_related(l1, Link, num=1)
[<Link: link 2>]
>>> TaggedItem.objects.get_related(l4, Link)
[]

# Related instance of a different Model
>>> a1 = Article.objects.create(name='article 1')
>>> Tag.objects.update_tags(a1, 'tag1 tag2 tag3 tag4')
>>> TaggedItem.objects.get_related(a1, Link)
[<Link: link 1>, <Link: link 2>, <Link: link 3>]
>>> Tag.objects.update_tags(a1, 'tag6')
>>> TaggedItem.objects.get_related(a1, Link)
[]
"""