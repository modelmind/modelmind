QUERY="""
WITH base_data AS (
  SELECT
    p.biographics_personality_mbti_type,
    r.result_label,
    p.biographics_personality_mbti_confidence
  FROM
    `modelmind.results.{questionnaire_id}` r
  JOIN
    `modelmind.firestore_sync.profiles_schema_views_latest` p
  ON
    r.result_id = p.results_member
  WHERE
    p.biographics_personality_mbti_type IS NOT NULL
),
total_predictions AS (
  SELECT
    COUNT(*) AS total_predictions,
    SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) AS correct_predictions,
    100.0 * SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) / COUNT(*) AS accuracy_percentage
  FROM
    base_data
),
confidence_above_0 AS (
  SELECT
    COUNT(*) AS total_predictions,
    SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) AS correct_predictions,
    100.0 * SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) / COUNT(*) AS accuracy_percentage
  FROM
    base_data
  WHERE
    biographics_personality_mbti_confidence > 0
),
confidence_above_1 AS (
  SELECT
    COUNT(*) AS total_predictions,
    SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) AS correct_predictions,
    100.0 * SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) / COUNT(*) AS accuracy_percentage
  FROM
    base_data
  WHERE
    biographics_personality_mbti_confidence > 1
),
confidence_above_2 AS (
  SELECT
    COUNT(*) AS total_predictions,
    SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) AS correct_predictions,
    100.0 * SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) / COUNT(*) AS accuracy_percentage
  FROM
    base_data
  WHERE
    biographics_personality_mbti_confidence > 2
),
confidence_above_3 AS (
  SELECT
    COUNT(*) AS total_predictions,
    SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) AS correct_predictions,
    100.0 * SUM(CASE WHEN biographics_personality_mbti_type = result_label THEN 1 ELSE 0 END) / COUNT(*) AS accuracy_percentage
  FROM
    base_data
  WHERE
    biographics_personality_mbti_confidence > 3
)
SELECT
  'total' AS confidence_level,
  0 AS sort_order,
  t.total_predictions,
  t.correct_predictions,
  t.accuracy_percentage
FROM
  total_predictions t
UNION ALL
SELECT
  '>=1' AS confidence_level,
  1 AS sort_order,
  c0.total_predictions,
  c0.correct_predictions,
  c0.accuracy_percentage
FROM
  confidence_above_0 c0
UNION ALL
SELECT
  '>=2' AS confidence_level,
  2 AS sort_order,
  c1.total_predictions,
  c1.correct_predictions,
  c1.accuracy_percentage
FROM
  confidence_above_1 c1
UNION ALL
SELECT
  '>=3' AS confidence_level,
  3 AS sort_order,
  c2.total_predictions,
  c2.correct_predictions,
  c2.accuracy_percentage
FROM
  confidence_above_2 c2
UNION ALL
SELECT
  '>=4' AS confidence_level,
  4 AS sort_order,
  c3.total_predictions,
  c3.correct_predictions,
  c3.accuracy_percentage
FROM
  confidence_above_3 c3
ORDER BY
  sort_order;
"""
