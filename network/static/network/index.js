document.addEventListener("DOMContentLoaded", function () {
  post_details();
});

function post_details() {
  fetch(`/post`);
  const element = document.createElement("div");

  // Add some HTML in the container to display the information of a specific email
  element.innerHTML = `<div class="post card">
        <div class="card-body">
            <p><a class="post-poster card-title" href="{% url 'profile' post.poster.username %}">${post.poster}</a></p>
            <p class="post-body card-text">${post.content}</p>
            <p class="post-creation-date card-text">
            <small class="text-muted">${post.creation_date}</small>
            </p>
            <p>number of like: ${like}</p>
        </div>
        </div>`;

  // Add the new HTML to the div email-details
  document.querySelector("#post-view").append(element);
}

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
