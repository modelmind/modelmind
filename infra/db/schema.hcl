schema "public" {
  comment = "Core domain schema for Personality Inventories and Assessment System"
}

// Core inventory tables
table "inventories" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "user_id" {
    type = text
    null = false
  }
  column "title" {
    type = varchar(255)
    null = false
  }
  column "description" {
    type = text
    null = true
  }
  column "version" {
    type = varchar(50)
    null = false
    default = "1.0"
  }
  column "status" {
    type = varchar(50)
    null = false
    default = "DRAFT"
    check = "status IN ('DRAFT','PUBLISHED','ARCHIVED')"
  }
  column "created_at" {
    type = timestamp
    null = false
    default = now()
  }
  column "updated_at" {
    type = timestamp
    null = false
    default = now()
  }

  primary_key {
    columns = ["id"]
  }
}

table "inventory_settings" {
  schema = schema.public
  column "inventory_id" {
    type = uuid
    null = false
  }
  column "randomize_items" {
    type = boolean
    null = false
    default = false
  }
  column "show_progress" {
    type = boolean
    null = false
    default = true
  }
  column "time_limit" {
    type = interval
    null = true
  }
  column "allow_back_navigation" {
    type = boolean
    null = false
    default = true
  }
  column "show_results" {
    type = boolean
    null = false
    default = true
  }
  column "results_format" {
    type = jsonb
    null = true
  }
  column "adaptive_testing" {
    type = boolean
    null = false
    default = false
  }
  column "metadata" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["inventory_id"]
  }

  foreign_key "inventory_fk" {
    columns = ["inventory_id"]
    ref_columns = ["inventories.id"]
    on_delete = "CASCADE"
  }
}

table "scales" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "inventory_id" {
    type = uuid
    null = false
  }
  column "name" {
    type = varchar(255)
    null = false
  }
  column "description" {
    type = text
    null = true
  }
  column "type" {
    type = varchar(50)
    null = false
    default = "STANDARD"
    check = "type IN ('STANDARD','COMPOSITE','DERIVED')"
  }
  column "metadata" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "inventory_fk" {
    columns = ["inventory_id"]
    ref_columns = ["inventories.id"]
    on_delete = "CASCADE"
  }

  unique {
    columns = ["inventory_id", "name"]
  }
}

table "items" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "inventory_id" {
    type = uuid
    null = false
  }
  column "title" {
    type = varchar(255)
    null = true
  }
  column "description" {
    type = text
    null = true
  }
  column "type" {
    type = varchar(50)
    null = false
    check = "type IN ('QUESTION','IMAGE','VIDEO','TEXT','PAGE_BREAK')"
  }
  column "order" {
    type = int
    null = false
    default = 0
  }
  column "required" {
    type = boolean
    null = false
    default = true
  }
  column "conditional_display" {
    type = jsonb
    null = true
    comment = "Rules for when this item should be displayed"
  }
  column "metadata" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "inventory_fk" {
    columns = ["inventory_id"]
    ref_columns = ["inventories.id"]
    on_delete = "CASCADE"
  }
}

table "question_items" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "item_id" {
    type = uuid
    null = false
  }
  column "question_type" {
    type = varchar(50)
    null = false
    check = "question_type IN ('TEXT','SCALE','MULTIPLE_CHOICE','LIKERT','RATING','IQ','MATRIX')"
  }
  column "settings" {
    type = jsonb
    null = false
    comment = "Type-specific settings (e.g., scale range, options, etc.)"
  }
  column "validation_rules" {
    type = jsonb
    null = true
    comment = "Response validation rules"
  }
  column "scoring_rules" {
    type = jsonb
    null = true
    comment = "Basic scoring rules if not using advanced scoring system"
  }
  column "feedback_correct" {
    type = text
    null = true
  }
  column "feedback_incorrect" {
    type = text
    null = true
  }
  column "time_limit" {
    type = interval
    null = true
  }
  column "difficulty_level" {
    type = decimal
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "item_fk" {
    columns = ["item_id"]
    ref_columns = ["items.id"]
    on_delete = "CASCADE"
  }

  unique {
    columns = ["item_id"]
  }
}

// Advanced Scoring System Tables
table "scoring_systems" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "scale_id" {
    type = uuid
    null = false
  }
  column "name" {
    type = varchar(255)
    null = false
  }
  column "description" {
    type = text
    null = true
  }
  column "type" {
    type = varchar(50)
    null = false
    check = "type IN ('SIMPLE','FORMULA','SCRIPT','RULE_BASED','ML_MODEL')"
  }
  column "active" {
    type = boolean
    null = false
    default = true
  }
  column "metadata" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "scale_fk" {
    columns = ["scale_id"]
    ref_columns = ["scales.id"]
    on_delete = "CASCADE"
  }
}

table "scoring_formulas" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "scoring_system_id" {
    type = uuid
    null = false
  }
  column "formula_type" {
    type = varchar(50)
    null = false
    check = "formula_type IN ('MATHEMATICAL','STATISTICAL','CONDITIONAL','CUSTOM')"
  }
  column "formula_definition" {
    type = jsonb
    null = false
  }
  column "raw_formula" {
    type = text
    null = true
  }
  column "metadata" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "scoring_system_fk" {
    columns = ["scoring_system_id"]
    ref_columns = ["scoring_systems.id"]
    on_delete = "CASCADE"
  }
}

table "scoring_rules" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "scoring_system_id" {
    type = uuid
    null = false
  }
  column "condition" {
    type = jsonb
    null = false
  }
  column "action" {
    type = jsonb
    null = false
  }
  column "priority" {
    type = int
    null = false
    default = 0
  }
  column "description" {
    type = text
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "scoring_system_fk" {
    columns = ["scoring_system_id"]
    ref_columns = ["scoring_systems.id"]
    on_delete = "CASCADE"
  }
}

table "scoring_scripts" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "scoring_system_id" {
    type = uuid
    null = false
  }
  column "language" {
    type = varchar(50)
    null = false
    check = "language IN ('JAVASCRIPT','PYTHON')"
  }
  column "script_content" {
    type = text
    null = false
  }
  column "input_schema" {
    type = jsonb
    null = false
  }
  column "output_schema" {
    type = jsonb
    null = false
  }
  column "version" {
    type = varchar(50)
    null = false
    default = "1.0"
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "scoring_system_fk" {
    columns = ["scoring_system_id"]
    ref_columns = ["scoring_systems.id"]
    on_delete = "CASCADE"
  }
}

table "scoring_variables" {
  schema = schema.public
  column "id" {
    type = uuid
    null = false
    default = gen_random_uuid()
  }
  column "scoring_system_id" {
    type = uuid
    null = false
  }
  column "name" {
    type = varchar(255)
    null = false
  }
  column "type" {
    type = varchar(50)
    null = false
    check = "type IN ('ITEM_RESPONSE','CALCULATED','CONSTANT','EXTERNAL')"
  }
  column "source" {
    type = jsonb
    null = false
  }
  column "description" {
    type = text
    null = true
  }

  primary_key {
    columns = ["id"]
  }

  foreign_key "scoring_system_fk" {
    columns = ["scoring_system_id"]
    ref_columns = ["scoring_systems.id"]
    on_delete = "CASCADE"
  }

  unique {
    columns = ["scoring_system_id", "name"]
  }
}

// Media Items Tables
table "image_items" {
  schema = schema.public
  column "item_id" {
    type = uuid
    null = false
  }
  column "alt_text" {
    type = varchar(255)
    null = true
  }
  column "source_uri" {
    type = text
    null = false
  }
  column "properties" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["item_id"]
  }

  foreign_key "item_fk" {
    columns = ["item_id"]
    ref_columns = ["items.id"]
    on_delete = "CASCADE"
  }

  check = "(SELECT type FROM items WHERE items.id = item_id) = 'IMAGE'"
}

table "video_items" {
  schema = schema.public
  column "item_id" {
    type = uuid
    null = false
  }
  column "youtube_uri" {
    type = text
    null = false
  }
  column "caption" {
    type = text
    null = true
  }
  column "properties" {
    type = jsonb
    null = true
  }

  primary_key {
    columns = ["item_id"]
  }

  foreign_key "item_fk" {
    columns = ["item_id"]
    ref_columns = ["items.id"]
    on_delete = "CASCADE"
  }

  check = "(SELECT type FROM items WHERE items.id = item_id) = 'VIDEO'"
}

table "text_items" {
  schema = schema.public
  column "item_id" {
    type = uuid
    null = false
  }
  column "content" {
    type = text
    null = false
  }
  column "format" {
    type = varchar(50)
    null = false
    default = 'PLAIN'
    check = "format IN ('PLAIN','HTML','MARKDOWN')"
  }

  primary_key {
    columns = ["item_id"]
  }

  foreign_key "item_fk" {
    columns = ["item_id"]
    ref_columns = ["items.id"]
    on_delete = "CASCADE"
  }

  check = "(SELECT type FROM items WHERE items.id = item_id) = 'TEXT'"
}
