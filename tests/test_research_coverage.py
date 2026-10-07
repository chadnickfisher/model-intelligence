from copy import deepcopy
from tools.knowledge import canonical, research_coverage_errors


def ledger():
    return [{'id':'check-'+d,'model_id':'example','domain':d,
             'checked_at':None,'result':'not_checked','evidence_ids':[],
             'search_references':[],'remaining_gaps':['Pending actual check'],
             'blocked_reason':None} for d in ['capabilities','benchmarks','access_pricing','behavior']]


def test_accounting_requires_every_model_domain_and_explicit_unchecked():
    records=ledger()
    assert not research_coverage_errors(records,{'example'},{})
    assert research_coverage_errors(records[:-1],{'example'},{})
    assert research_coverage_errors(records+[deepcopy(records[0])],{'example'},{})
    records[0]['checked_at']='2026-10-07'
    assert any('unchecked' in e for e in research_coverage_errors(records,{'example'},{}))


def test_actual_check_requires_references_and_rejects_carry_forward_dates():
    records=ledger();r=records[0]
    r.update(result='unchanged',checked_at='2026-10-07',evidence_ids=['source1'])
    sources={'source1':{'accessed_at':'2026-10-06'}}
    assert any('predates' in e for e in research_coverage_errors(records,{'example'},sources))
    sources['source1']['accessed_at']='2026-10-07'
    assert not research_coverage_errors(records,{'example'},sources)
    r['evidence_ids']=[]
    assert any('references' in e for e in research_coverage_errors(records,{'example'},sources))


def test_no_matched_reports_remain_unknown_and_blocked_is_explained():
    records=ledger();r=records[0]
    r.update(result='unknown',checked_at='2026-10-07',search_references=[
        {'query':'example postlaunch reports','checked_at':'2026-10-07','outcome':'no_matched_sources','urls':[],'notes':[]}])
    assert not research_coverage_errors(records,{'example'},{})
    r['search_references'][0]['checked_at']='2026-10-06'
    assert any('dates differ' in e for e in research_coverage_errors(records,{'example'},{}))
    r.update(result='blocked',search_references=[],blocked_reason=None)
    assert any('reason' in e for e in research_coverage_errors(records,{'example'},{}))
    r['blocked_reason']='Public source returned HTTP 403'
    assert not research_coverage_errors(records,{'example'},{})


def test_catalog_ledger_accounts_for_all_53_models_without_fabricated_checks():
    current=canonical()
    model_ids={i for k,i in current if k=='model'}
    records=[r for (k,_),(_,r) in current.items() if k=='research_coverage']
    sources={i:r for (k,i),(_,r) in current.items() if k=='source'}
    assert len(records)==len(model_ids)*4
    assert not research_coverage_errors(records,model_ids,sources)
