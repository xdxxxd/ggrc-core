# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
update propagation tree for program editor

Create Date: 2019-09-15 12:09:24.688154
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from ggrc.migrations.utils.acr_propagation import update_acr_propagation_tree

# revision identifiers, used by Alembic.
revision = '3141784ef298'
down_revision = '8937c6e26f00'

PROGRAM_EDITOR_PERMISSIONS = {
    "AccessGroup RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "AccountBalance RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Audit RU": {
        "Relationship R": {
            "Assessment RU": {
                "Relationship R": {
                    "Comment R": {},
                    "Evidence RU": {
                        "Relationship R": {
                            "Comment R": {}
                        }
                    }
                }
            },
            "AssessmentTemplate RUD": {},
            "Evidence RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Issue RUD": {
                "Relationship R": {
                    "Comment R": {},
                    "Document RU": {
                        "Relationship R": {
                            "Comment R": {}
                        }
                    }
                }
            },
            "Snapshot RU": {}
        }
    },
    "Comment R": {},
    "Contract RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "Control RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Proposal RU": {},
            "Review RU": {}
        }
    },
    "DataAsset RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Document RU": {
        "Relationship R": {
            "Comment R": {}
        }
    },
    "Facility RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Issue RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "KeyReport RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Market RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Metric RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Objective RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "OrgGroup RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Policy RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "Process RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Product RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "ProductGroup RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Project RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Proposal R": {},
    "Regulation RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "Requirement RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "Review RU": {},
    "Risk RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Proposal RU": {},
            "Review RU": {}
        }
    },
    "Standard RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "System RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "TechnologyEnvironment RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    },
    "Threat RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            },
            "Review RU": {}
        }
    },
    "Vendor RU": {
        "Relationship R": {
            "Comment R": {},
            "Document RU": {
                "Relationship R": {
                    "Comment R": {}
                }
            }
        }
    }
}


RELATIONSHIP = {"Relationship R": PROGRAM_EDITOR_PERMISSIONS}

PROGRAM_EDITORS = {"Program Editors": RELATIONSHIP}

CONTROL_PROPAGATION = {
    "Program": PROGRAM_EDITORS
}

OLD_CONTROL_PROPAGATION = {
    "Program": PROGRAM_EDITORS
}


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  update_acr_propagation_tree(OLD_CONTROL_PROPAGATION, CONTROL_PROPAGATION)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
