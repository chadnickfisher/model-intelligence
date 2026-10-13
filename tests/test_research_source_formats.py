"""Observed untitled/PDF returns and complete independent page versions."""
from hashlib import sha256

import pytest

from test_research_source_bodies import bundle, save, result, page
from test_research_batch import SID
from tools import research_source_bodies as bodies


def test_untitled_numbered_page_keeps_identity_and_requires_all_lines(tmp_path):
    files=bundle(tmp_path);url=files[3]
    save(files[1],url,page(url,0,2).replace('Methods (',' (',1))
    assert result(files)['checks']['SB07']=='failed'
    save(files[1],url,page(url,1,3).replace('Methods (',' (',1))
    assert result(files)['status']=='source_bodies_verified'
    with pytest.raises(ValueError,match='identity'):
        bodies.page_lines(bodies.encoded(page(url).replace(url,url+'/other')),url)


def test_untitled_pdf_page_and_page_range_labels_merge_without_rewriting(tmp_path):
    files=bundle(tmp_path);url=files[3]
    first=' ('+url+')\nTotal lines: 4\nL0@P0: Heading\nL1@P0: First\nL2@P0-1: Across pages'
    last=' ('+url+')\nTotal lines: 4\nL2@P0-1: Across pages\nL3@P1: Last'
    save(files[1],url,first)
    assert result(files)['checks']['SB07']=='failed'
    save(files[1],url,last)
    captures={};audit=result(files,captures=captures)
    assert audit['status']=='source_bodies_verified'
    assert captures[SID]['text']=='Heading\nFirst\nAcross pages\nLast\n'
    assert bodies.parse((files[1].parent/'responses/source-000001.json').read_bytes())==first
    save(files[1],url,last.replace('Across pages','Conflicting page text'))
    assert result(files)['checks']['SB07']=='failed'


def test_two_independently_complete_versions_retain_history_and_latest_body(tmp_path):
    files=bundle(tmp_path);url=files[3]
    save(files[1],url,page(url))
    latest='Methods ('+url+')\nTotal lines: 2\nL0: Cookie settings\nL1: Current methods'
    save(files[1],url,latest)
    captures={};audit=result(files,captures=captures)
    assert audit['status']=='source_bodies_verified'
    assert captures[SID]['text']=='Cookie settings\nCurrent methods\n'
    history=audit['sources'][SID]['source_capture']['prior_versions']
    assert history[0]['call_ids']==['source-000001']
    assert history[0]['visible_line_count']==3
    assert history[0]['text_sha256']==sha256(b'Published original methods\nExact model checkpoint and effort setting.\nMethods complete.\n').hexdigest()
    assert audit['sources'][SID]['source_capture']['call_ids']==['source-000002']


@pytest.mark.parametrize('first,last',[(False,True),(True,False)])
def test_changed_partial_versions_cannot_be_joined_or_discarded(tmp_path,first,last):
    files=bundle(tmp_path);url=files[3]
    save(files[1],url,page(url,0,3 if first else 2))
    changed=page(url,0,3 if last else 2).replace('Published original methods','Changed title')
    save(files[1],url,changed)
    assert result(files)['status']=='source_bodies_incomplete'
    assert result(files)['checks']['SB07']=='failed'


def test_lost_return_with_unknown_times_remains_failed_after_successful_retry(tmp_path):
    files=bundle(tmp_path);url=files[3]
    bodies.capture(files[1],source_id=SID,url=url,tool='observed-source',started_at=None,
        completed_at=None,request={'open':[{'ref_id':url}]},response_path=None,retrieval_status='unavailable')
    save(files[1],url,page(url))
    audit=result(files)
    assert audit['checks']['SB04']=='failed' and audit['checks']['SB10']=='failed'
    assert audit['status']=='source_bodies_incomplete'


@pytest.mark.parametrize('prior_text',['', 'x'*(bodies.MAX_TEXT+1)],ids=['empty','oversized'])
def test_complete_new_version_cannot_hide_invalid_prior_body(tmp_path,prior_text):
    files=bundle(tmp_path);url=files[3]
    prior='Methods ('+url+')\nTotal lines: 1\nL0: '+prior_text
    save(files[1],url,prior)
    save(files[1],url,page(url))
    audit=result(files)
    assert audit['status']=='source_bodies_incomplete'
    assert audit['checks']['SB07']=='failed'
