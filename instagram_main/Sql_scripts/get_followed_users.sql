SELECT distinct igp.ig_id,igi.followed_username,igi.date_followed FROM public."IG_iamfollowing" as igi
INNER join  "IG_profile_details" as igp
on igp.ig_id = igi.ig_id
where igp.account_user = 'textToReplace'
and igi.unfollowed_username is NULL
order by igi.date_followed desc
fetch FIRST 150 ROWS ONLY