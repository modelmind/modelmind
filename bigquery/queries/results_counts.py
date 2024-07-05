QUERY="""
SELECT
  r.result_label AS label,
  COUNT(*) AS counts,
  SUM(CASE WHEN p.biographics_gender = 'male' THEN 1 ELSE 0 END) AS male,
  SUM(CASE WHEN p.biographics_gender = 'female' THEN 1 ELSE 0 END) AS female,
  SUM(CASE WHEN p.biographics_gender NOT IN ('male', 'female') THEN 1 ELSE 0 END) AS other
FROM
  `modelmind.results.{questionnaire_id}` r
JOIN
  `modelmind.firestore_sync.profiles_schema_views_latest` p
ON
  r.result_id = p.results_member
GROUP BY
  r.result_label
ORDER BY
  r.result_label;
"""
