document.addEventListener("DOMContentLoaded", function () {
  function follow_profile(profile_id, user_id) {
    // follow a profile by  email by changing status Archive = True
    fetch(`/post/${profile_id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: true,
      }),
    }).then((result) => {
      // Then load the Archive Mailbox
      load_mailbox("archive");
    });
    return false;
  }
});
