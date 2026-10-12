"""Evidence authoring directions stay aligned with actual retained-source review guards."""
from copy import deepcopy
from hashlib import sha256
import json

import pytest
from test_research_batch import baseline, fixture, TODAY
from test_research_review import review_request, answer
from tools import research_batch as batch, research_output_contract as output, research_review as review




def test_semantic_rules_name_real_review_checks_and_schema_permitted_paths():
    schemas=batch.schema_registry()[0]
    contract=output.build_contract(schemas,TODAY)
    assert set(contract['evidence_review']['checks'])=={'EV01','EV02','EV03','EV04'}
    for rule in contract['evidence_review']['rules'].values():
        assert set(rule['review_checks']) <= set(review.CHECKS)
        for kind,paths in rule['record_paths'].items():
            allowed={row['path'] for row in contract['records'][kind]['fields']}
            assert set(paths) <= allowed,(kind,set(paths)-allowed)
    guide=output.render_contract(contract).decode()
    assert 'not portable schema/mechanical attestation' in guide
    for ident,rule in contract['evidence_review']['rules'].items():
        assert '| '+ident+' | '+output.EVIDENCE_CHECKS[ident]+' |' in guide
        assert all(entry in guide for entry in rule['save'])






def test_receiver_request_carries_exact_evidence_rules(review_request):
    request,_,digest=review_request
    assert request['evidence_checks']==output.evidence_review_contract()
    assert 'exact result row' in request['policy'] and 'each evaluator' in request['policy']
    assert review.validate_response(answer(request,digest),request,digest)
    request=deepcopy(request); request['evidence_checks']['rules'].pop('EV01')
    digest=sha256(review.encoded(request)).hexdigest()
    with pytest.raises(ValueError,match='Evidence review contract differs'):
        review.validate_response(answer(request,digest),request,digest)


@pytest.mark.parametrize('kind',['price','access','model','provider'])
def test_configuration_and_offer_checks_cannot_be_marked_inapplicable(review_request,kind):
    request,_,_=review_request; request=deepcopy(request)
    request['units'][0]['kind']=kind
    digest=sha256(review.encoded(request)).hexdigest()
    response=answer(request,digest)
    response['decisions'][0]['checks']['setup']='not_applicable'
    with pytest.raises(ValueError,match='EV03/EV04'):
        review.validate_response(response,request,digest)
