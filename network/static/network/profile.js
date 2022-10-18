document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#followingButtons")
    .addEventListener("click", function () {
      console.log("button clicked");
    });
});

// function follow_profile(profile) {
//   // Archive an email by changing status Archive = True
//   fetch(`/profile/${profile}`, {
//     method: "POST",
//     body: JSON.stringify({
//       archived: true,
//     }),
//   }).then((result) => {
//     // Then load the Archive Mailbox
//     load_mailbox("archive");
//   });
//   return false;
// }
