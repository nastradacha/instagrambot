SELECT igp.ig_id ,followed_username FROM public."IG_iamfollowing" as igi
INNER join  "IG_profile_details" as igp
on igp.ig_id = igi.ig_id
where igp.account_user = 'textToReplace'