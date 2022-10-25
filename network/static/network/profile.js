document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#profile-view").style.display = "none";
  document.querySelector("#all-post").style.display = "block";
  document
    .querySelector("#followingButtons")
    .addEventListener("click", () => display_profile("1234"));
});

function display_profile(profile) {
  document.querySelector("#profile-view").style.display = "block";
  document.querySelector("#all-post").style.display = "none";

  // Call the API to get the details of the profile
  fetch(`/profile/${profile}`)
    .then((response) => response.json())
    .then((profile) => {
      // Create the container to show the email details
      profile_details(profile);
      follow_actions(profile);
      profile_posts(profile);
    });
}

function profile_details(profile) {
  const element = document.createElement("div");

  // Add some HTML in the container to display the information of a specific email
  element.innerHTML = `<div class="user">
      <h2 id="profile">user : ${profile.username}</h2>
    </div>

    <div id="profile-details" class="profile">
      <ul>
        <li>Name: ${profile.firstname} ${profile.lastname}</li>
        <li>Account created : ${profile.accountCreated}</li>

        <li>Number of followers: ${profile.follower}</li>
        <li>Following: ${profile.followed}</li>
        <li>Is it currently following : ${profile.isFollowing}</li>
        <li>Is it own profile : ${profile.isOwnProfile}</li>
      </ul>
    </div>`;

  // Add the new HTML to the div email-details
  document.querySelector("#profile-view").append(element);
}

function profile_posts(profile) {
  profile.posts.forEach(function (post) {
    const element = document.createElement("div");

    element.innerHTML = `<div class="posts">
     <div class="post">
      <p>${profile.username}</p>
      <p>${post.fields.content}</p>
      <p>${post.fields.creation_date}</p>
     </div>
     </div>`;

    document.querySelector("#profile-posts").append(element);
  });
}

function follow_profile(profile) {
  fetch(`/profile/${profile.username}`, {
    method: "POST",
  }).then((result) => {
    console.log(result);
    display_profile(profile.username);
  });
  return false;
}

function unfollow_profile(profile) {
  fetch(`/profile/${profile.username}`, {
    method: "DELETE",
  }).then((result) => {
    console.log(result);
    display_profile(profile.username);
  });
  return false;
}

function check_follow(profile) {
  if (profile.isFollowing) {
    return unfollow_profile(profile);
  } else {
    return follow_profile(profile);
  }
}

function follow_actions(profile) {
  const element = document.createElement("div");
  element.innerHTML = `<div class="action-buttons">
  <button id="followButtons">${
    profile.isFollowing ? "Unfollow" : "Follow"
  }</button>  </div>`;

  document.querySelector("#profile-follow").append(element);

  document
    .querySelector("#followButtons")
    .addEventListener("click", function () {
      check_follow(profile);
    });
}
