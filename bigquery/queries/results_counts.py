QUERY="""
SELECT
  COUNT(*) AS total,
  COUNT(p.biographics_personality_mbti_type) AS with_label,
  SUM(CASE WHEN p.biographics_gender = 'male' THEN 1 ELSE 0 END) AS male,
  SUM(CASE WHEN p.biographics_gender = 'female' THEN 1 ELSE 0 END) AS female,
  SUM(CASE WHEN p.biographics_gender NOT IN ('male', 'female') THEN 1 ELSE 0 END) AS other
FROM
  `modelmind.results.{questionnaire_id}` r
JOIN
  `modelmind.firestore_sync.profiles_schema_views_latest` p
ON
  r.result_id = p.results_member;
"""
