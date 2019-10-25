# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration test for With Custom Restrictions mixin"""

import collections
import ddt

from flask import g

from ggrc import db
from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories
from integration.ggrc.query_helper import WithQueryApi


# pylint: disable=invalid-name
@ddt.ddt
class TestWithCustomRestrictions(TestCase, WithQueryApi):
  """Test cases for With Custom Restrictions mixin"""

  def setUp(self):
    super(TestWithCustomRestrictions, self).setUp()
    self.client.get("/login")
    self.api = Api()

  @staticmethod
  def assign_person(object_, acr, person_id):
    """Assign person to object."""
    # pylint: disable=protected-access
    for ac_list in object_._access_control_list:
      if ac_list.ac_role.name == acr.name and acr.object_type == object_.type:
        factories.AccessControlPersonFactory(
            person_id=person_id,
            ac_list=ac_list,
        )

  @staticmethod
  def set_current_person(user):
    """Set user as current for Flask app"""
    setattr(g, '_current_user', user)

  @ddt.data(
      ('Assignees', True),
      ('Creators', False),
      ('Verifiers', False),
      ("Primary Contacts", False),
      ("Secondary Contacts", False)
  )
  @ddt.unpack
  def test_assignee_has_restricted_access(self, role_name, restricted_access):
    # pylint: disable=protected-access
    """Test Assignee role restricted access to fields for Assessment
    with sox302"""
    assmnt = factories.AssessmentFactory(sox_302_enabled=True)
    person = factories.PersonFactory()
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name=role_name,
        object_type="Assessment",
    ).first()
    self.assign_person(assmnt, acr_assmnt, person.id)
    user = next(self.get_persons_for_role_name(assmnt, role_name))
    self.set_current_person(user)
    self.assertEqual(assmnt._is_sox_restricted(), restricted_access)

  @ddt.data("Audit Captains", "Auditors")
  def test_propagated_audit_roles(self, audit_role):
    """Test user sox302 permissions for Assessment with roles in Audit
    and Assessment"""
    user = factories.PersonFactory()
    acr_audit = all_models.AccessControlRole.query.filter_by(
        name=audit_role,
        object_type="Audit",
    ).first()
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()

    audit = factories.AuditFactory()
    self.assign_person(audit, acr_audit, user.id)

    assessment = factories.AssessmentFactory(audit=audit, sox_302_enabled=True)
    self.assign_person(assessment, acr_assmnt, user.id)
    factories.RelationshipFactory(
        source=audit, destination=assessment
    )

    self.assertFalse(assessment.is_user_role_restricted(user))

  @ddt.data("Program Managers", "Program Editors")
  def test_propagated_program_roles(self, program_role):
    """Test user sox302 permissions for Assessment with roles in Program
    and Assessment"""
    user = factories.PersonFactory()
    acr_program = all_models.AccessControlRole.query.filter_by(
        name=program_role,
        object_type="Program",
    ).first()
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()

    program = factories.ProgramFactory()
    self.assign_person(program, acr_program, user.id)

    audit = factories.AuditFactory(program=program)
    factories.RelationshipFactory(
        source=audit,
        destination=program,
    )

    assessment = factories.AssessmentFactory(audit=audit, sox_302_enabled=True)
    self.assign_person(assessment, acr_assmnt, user.id)
    factories.RelationshipFactory(
        source=audit, destination=assessment
    )

    self.assertFalse(assessment.is_user_role_restricted(user))

  @ddt.data(
      (
          True,
          ['access_control_list',
           'description',
           'title',
           'labels',
           'test_plan',
           'assessment_type',
           'slug',
           'notes',
           'start_date',
           'design',
           'operationally',
           'reminderType',
           'issue_tracker',
           'map: Snapshots',
           'map: Issue'],
      ),
      (
          False,
          [],
      ),
  )
  @ddt.unpack
  def test_get_302_sox_assmt(self, is_sox_restricted, ro_fields):
    """Test get sox302 assessment by api call returns proper values"""
    with factories.single_commit():
      user = factories.PersonFactory()
      assessment = factories.AssessmentFactory(
          sox_302_enabled=is_sox_restricted
      )
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)

    response = self.api.get(all_models.Assessment, assessment.id)

    self.assert200(response)
    res = response.json['assessment']
    self.assertEqual(is_sox_restricted, res['_is_sox_restricted'])
    self.assertEqual(ro_fields, res['_readonly_fields'])

  @ddt.data(
      ('Issue', {}),
  )
  @ddt.unpack
  def test_post_readonly_relationship(self, restricted_model, factory_args):
    """Test post mapping to readonly object is forbidden"""
    with factories.single_commit():
      user = factories.PersonFactory()
      restricted_obj = factories.get_model_factory(
          restricted_model)(**factory_args)
      assessment = factories.AssessmentFactory(sox_302_enabled=True)
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)
    assessment_id = assessment.id

    response = self.api.post(all_models.Relationship, {
        "relationship": {
            "source": {"id": assessment_id, "type": assessment.type},
            "destination": {
                "id": restricted_obj.id,
                "type": restricted_obj.type
            },
            "context": None
        },
    })

    self.assert405(response)

  def test_post_snapshot_mapping(self):
    """Test post mapping to Snapshot object is forbidden"""
    with factories.single_commit():
      audit = factories.AuditFactory()
      assessment = factories.AssessmentFactory(
          audit=audit,
          sox_302_enabled=True
      )
      assessment_id = assessment.id
      user = factories.PersonFactory()
      factories.RelationshipFactory(source=audit, destination=assessment)
      control = factories.ControlFactory()
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)
    revision = all_models.Revision.query.filter(
        all_models.Revision.resource_id == control.id,
        all_models.Revision.resource_type == control.__class__.__name__
    ).order_by(
        all_models.Revision.id.desc()
    ).first()
    snapshot = factories.SnapshotFactory(
        parent=audit,
        child_id=control.id,
        child_type=control.__class__.__name__,
        revision_id=revision.id
    )
    db.session.commit()

    response = self.api.post(all_models.Relationship, {
        "relationship": {
            "source": {"id": assessment_id, "type": assessment.type},
            "destination": {"id": snapshot.id, "type": snapshot.type},
            "context": None
        },
    })

    self.assert405(response)

  def test_put_snapshot_mapping(self):
    """Test put mapping to Snapshot object is forbidden"""
    with factories.single_commit():
      audit = factories.AuditFactory()
      assessment = factories.AssessmentFactory(
          audit=audit,
          sox_302_enabled=True
      )
      user = factories.PersonFactory()
      factories.RelationshipFactory(source=audit, destination=assessment)
      control = factories.ControlFactory()
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)
    revision = all_models.Revision.query.filter(
        all_models.Revision.resource_id == control.id,
        all_models.Revision.resource_type == control.__class__.__name__
    ).order_by(
        all_models.Revision.id.desc()
    ).first()
    snapshot = factories.SnapshotFactory(
        parent=audit,
        child_id=control.id,
        child_type=control.__class__.__name__,
        revision_id=revision.id
    )
    db.session.commit()

    response = self.api.put(assessment, {"actions": {"add_related": [
        {
            "id": snapshot.id,
            "type": snapshot.type,
        }
    ]}})

    self.assert405(response)

  def test_post_issue_not_mapped(self):
    """Test posted issue not mapped automatically"""
    with factories.single_commit():
      user = factories.PersonFactory()
      assessment = factories.AssessmentFactory(sox_302_enabled=True)
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)

    response = self.api.post(all_models.Issue, data={
        "issue": {
            "title": "TestDueDate",
            "context": None,
            "due_date": "06/14/2018",
            "assessment": {
                "id": assessment.id,
                "type": assessment.type,
            },
        }
    })

    self.assert405(response)

  def test_update_restricted_assessment(self):  # fill necessary fields values
    """Test user sox302 permissions to update restricted Assessment"""
    with factories.single_commit():
      user = factories.PersonFactory()
      assessment = factories.AssessmentFactory(sox_302_enabled=True)
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)

    response = self.api.put(assessment, {"status": "In Progress"})

    self.assert405(response)

  def test_import_sox302_assmt_ro_field(self):
    """Test user sox302 update read only fields via import"""
    exp_errors = {}  # Add expected errors
    with factories.single_commit():
      user = factories.PersonFactory()
      assessment = factories.AssessmentFactory(sox_302_enabled=True)
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)

    response = self.import_data(collections.OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", assessment.slug),
        ("Title", "TestTitle"),
    ]))

    self._check_csv_response(response, exp_errors)

  def test_import_sox302_assmt_mapping_issue(self):
    """Test user sox302 update restricted mappings"""
    exp_errors = {}  # Add expected errors
    with factories.single_commit():
      user = factories.PersonFactory()
      assessment = factories.AssessmentFactory(sox_302_enabled=True)
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)
    issue = factories.IssueFactory()

    response = self.import_data(collections.OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", assessment.slug),
        ("map: Issue", issue.slug),
    ]))

    self._check_csv_response(response, exp_errors)

  def test_import_sox302_assmt_mapping_snapshot(self):
    """Test user sox302 update restricted mappings"""
    exp_errors = {}  # Add expected errors
    with factories.single_commit():
      audit = factories.AuditFactory()
      assessment = factories.AssessmentFactory(
          audit=audit,
          sox_302_enabled=True
      )
      user = factories.PersonFactory()
      factories.RelationshipFactory(source=audit, destination=assessment)
      control = factories.ControlFactory()
    acr_assmnt = all_models.AccessControlRole.query.filter_by(
        name="Assignees",
        object_type="Assessment",
    ).first()
    self.assign_person(assessment, acr_assmnt, user.id)
    revision = all_models.Revision.query.filter(
        all_models.Revision.resource_id == control.id,
        all_models.Revision.resource_type == control.__class__.__name__
    ).order_by(
        all_models.Revision.id.desc()
    ).first()
    factories.SnapshotFactory(
        parent=audit,
        child_id=control.id,
        child_type=control.__class__.__name__,
        revision_id=revision.id
    )
    db.session.commit()

    response = self.import_data(collections.OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", assessment.slug),
        ("map:Control versions", control.slug),
    ]))

    self._check_csv_response(response, exp_errors)
