"""Record shape checks use the same schema-derived requirements given to authors."""
from argparse import Namespace
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from test_research_batch import baseline,fixture,TODAY
from test_research_search_receipts import evidence,new_session
from tools import research_batch as batch
from tools import research_output_contract as output
from tools.research_validation import Session,pin,verify_receipt


@pytest.fixture(scope='module')
def schemas():return batch.schema_registry()[0]


def test_portable_record_types_match_receiver():
    assert output.SCHEMAS==batch.SCHEMAS
    assert output.PREFIXES==batch.PREFIXES


def test_generated_required_nullable_key_and_provenance_branches(schemas):
    contract=output.build_contract(schemas,TODAY)
    label=next(row for row in contract['records']['access']['fields'] if row['path']=='/model_label')
    assert label['required_in_parent'] and label['nullable']
    assert label['schema_location']=='access-record.schema.json#/properties/model_label'
    provenance=[row for row in contract['records']['model']['fields']
                if row['path']=='/capabilities/*/provenance/research_batch_id']
    assert len(provenance)==1 and provenance[0]['required_in_parent'] and not provenance[0]['nullable']
    assert provenance[0]['conditions'][-1]['keyword']=='oneOf'
    guide=output.render_contract(contract).decode()
    assert '`/model_label` | Required | null, string | Yes' in guide
    assert '| RC03 | '+output.CHECKS['RC03']+' |' in guide


def test_conditional_evidence_and_confidence_rules_are_in_the_generated_guide(schemas):
    contract=output.build_contract(schemas,TODAY)
    rules=contract['records']['task_assessment']['conditional_rules']
    assert rules and any('then' in rule['clauses'] for rule in rules)
    guide=output.render_contract(contract).decode()
    for rule in rules:
        assert rule['schema_location'] in guide
        assert json.dumps(rule['clauses'],ensure_ascii=False,sort_keys=True,indent=2) in guide


def test_valid_proposals_are_checked_without_mutation(fixture,schemas):
    packet,_=fixture;before=deepcopy(packet)
    assert output.validate_records(packet,schemas,output.build_contract(schemas,TODAY))==[]
    assert packet==before


def test_four_missing_provenance_fields_and_nullable_key_are_all_reported(fixture,baseline,schemas):
    packet,_=fixture;packet=deepcopy(packet)
    model=next(c['record'] for c in packet['changes'] if c['kind']=='model')
    for n in range(4):
        finding=deepcopy(model['capabilities'][0]);finding['id']='new:synthetic-finding-'+str(n)
        finding['provenance']={'origin':'research','method':'Synthetic original-body inspection; no inference.'}
        model['capabilities'].append(finding)
    route=deepcopy(next(r for (kind,_),r in baseline.items() if kind=='access' and r['model_id']==model['id']))
    route['id']='new:synthetic-nullable-label';route.pop('model_label')
    packet['changes'].append({'kind':'access','record':route})
    before=deepcopy(packet)
    errors=output.validate_records(packet,schemas,output.build_contract(schemas,TODAY))
    assert len(errors)==5
    assert sum(e['missing_keys']==['research_batch_id'] for e in errors)==4
    assert sum(e['missing_keys']==['model_label'] for e in errors)==1
    assert all(e['check_id']=='RC03' for e in errors)
    assert packet==before
    for finding in model['capabilities'][-4:]:finding['provenance']['research_batch_id']='public-source-inspection-'+TODAY
    route['model_label']=None
    assert output.validate_records(packet,schemas,output.build_contract(schemas,TODAY))==[]


def test_unknown_kind_and_contract_drift_fail(schemas):
    contract=output.build_contract(schemas,TODAY)
    assert output.validate_records({'changes':[{'kind':'invented','record':{}}]},schemas,contract)[0]['check_id']=='RC02'
    contract['records']['access']['fields']=[]
    with pytest.raises(ValueError,match='RC01'):output.validate_records({'changes':[]},schemas,contract)


def record_session(evidence,tmp_path,schemas,changes):
    packet=json.loads(evidence[0].read_bytes());packet['changes']=changes
    evidence[0].write_bytes(output.encoded(packet))
    base,audit_path=new_session(evidence,tmp_path)
    kit=base.kit
    bundle={**schemas,'fixture':{'type':'object'}}
    contract=output.build_contract(bundle,TODAY)
    (kit/'schemas.json').write_bytes(output.encoded(bundle))
    (kit/'research_output_contract.py').write_bytes(Path(output.__file__).read_bytes())
    (kit/'output-contract.json').write_bytes(output.encoded(contract))
    (kit/'output-contract.md').write_bytes(output.render_contract(contract))
    manifest=json.loads((kit/'input-manifest.json').read_bytes())
    for name in ('schemas.json','research_output_contract.py','output-contract.json','output-contract.md'):
        manifest['files'][name]=pin((kit/name).read_bytes())
    (kit/'input-manifest.json').write_bytes(output.encoded(manifest))
    return Session(kit,base.args),audit_path


def test_v3_receipt_requires_record_validation_in_addition_to_search_capture(evidence,tmp_path,schemas):
    session,audit_path=record_session(evidence,tmp_path,schemas,[])
    session.schema('fixture');session.checks['mechanical']='passed'
    receipt=session.finish()
    assert receipt['format']=='research-validation-v3'
    assert receipt['checks']=={'schema':'passed','records':'passed','mechanical':'passed','search_receipts':'passed'}
    assert verify_receipt(receipt,session.raw,session.manifest_raw,sha256(session.manifest_raw).hexdigest(),
                          search_index_raw=evidence[1].read_bytes(),search_audit_raw=audit_path.read_bytes())['status']=='receipt_binding_verified'


def test_envelope_pass_cannot_hide_invalid_nested_record(evidence,tmp_path,schemas,baseline):
    model=deepcopy(next(r for (kind,_),r in baseline.items() if kind=='model'))
    model['capabilities'][0]['provenance']={'origin':'research','method':'Synthetic inspection'}
    session,_=record_session(evidence,tmp_path,schemas,[{'kind':'model','record':model}])
    with pytest.raises(ValueError,match='RC03'):session.schema('fixture')
    assert session.checks['schema']=='passed' and session.checks['records']=='failed'
    assert session.record_errors[0]['missing_keys']==['research_batch_id']
    assert not session.args.receipt.exists()


def test_human_guide_cannot_drift_from_machine_contract(evidence,tmp_path,schemas):
    session,_=record_session(evidence,tmp_path,schemas,[])
    session.inputs['output-contract.md']=b'Incomplete manually maintained guide'
    with pytest.raises(ValueError,match='RC01'):session.schema('fixture')
    assert session.checks['records']=='failed' and not session.args.receipt.exists()
