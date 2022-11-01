document.addEventListener("DOMContentLoaded", function () {});

//   function like_post(post){
//     fetch(`/update/${post.id}`,
//   }

//   function follow_profile(profile) {
//     fetch(`/update/${profile.username}`, {
//       method: "POST",
//     }).then((result) => {
//       display_profile(profile.username);
//       console.log(result);
//     });
//     return false;
//   }

//   function unfollow_profile(profile) {
//     fetch(`/update/${profile.username}`, {
//       method: "DELETE",
//     }).then((result) => {
//       display_profile(profile.username);
//       console.log(result);
//     });
//     return false;
//   }

//   function check_follow(profile) {
//     if (profile.isFollowing) {
//       return unfollow_profile(profile);
//     } else {
//       return follow_profile(profile);
//     }
//   }

//   function follow_actions(profile) {
//     if (profile.isOwnProfile) {
//       document.querySelector("#profile-follow").innerHTML = "";
//     } else {
//       const element = document.createElement("div");
//       element.innerHTML = `<div class="action-buttons">
//       <button class="btn btn-primary" id="followButtons">${
//         profile.isFollowing ? "Unfollow" : "Follow"
//       }</button>  </div>`;

//       document.querySelector("#profile-follow").append(element);

//       document
//         .querySelector("#followButtons")
//         .addEventListener("click", function () {
//           check_follow(profile);
//         });
//     }
//   }
