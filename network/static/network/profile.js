document.addEventListener("DOMContentLoaded", function () {
  function follow_profile(profile_id) {
    // follow a profile by  email by changing status Archive = True
    fetch(`/emails/${email_id}`, {
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
