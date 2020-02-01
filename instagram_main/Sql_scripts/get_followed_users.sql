SELECT distinct igp.ig_id,igi.followed_username,igi.date_followed FROM public."IG_iamfollowing" as igi
INNER join  "IG_profile_details" as igp
on igp.ig_id = igi.ig_id
where igp.account_user = 'textToReplace'
order by igi.date_followed asc
fetch FIRST 5 ROWS ONLY