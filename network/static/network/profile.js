document.addEventListener("DOMContentLoaded", function () {
  display_profile(document.querySelector("#poster").innerHTML);
});

function display_profile(profile) {
  document.querySelector("#profile-view").innerHTML = "";
  document.querySelector("#profile-follow").innerHTML = "";
  document.querySelector("#profile-posts").innerHTML = "";

  // Call the API to get the details of the profile
  fetch(`/update/${profile}`)
    .then((response) => response.json())
    .then((profile) => {
      // Create the container to show the email details
      profile_details(profile);
      follow_actions(profile);
    });
}

async function profile_details(profile) {
  const element = document.createElement("div");

  // Add some HTML in the container to display the information of a specific email
  element.innerHTML = `<div id="profile-details" class="profile card">
      <div class="card-body">
        <p class="card-text">Name: ${profile.firstname} ${profile.lastname}</p>
        <p>Account created : ${profile.accountCreated}</p>
        <div class="follow-data">
          <div class="follow-details">
            Number of followers: <span class="badge badge-primary badge-pill">${profile.follower}</span>
          </div>
          <div class="follow-details">
            Following: <span class="badge badge-primary badge-pill">${profile.followed}</span>
          </div>
        </div>
        
      </div>
    </div>`;

  // Add the new HTML to the div email-details
  document.querySelector("#profile-view").append(element);
}

function follow_profile(profile) {
  fetch(`/update/${profile.username}`, {
    method: "POST",
  }).then((result) => {
    display_profile(profile.username);
    console.log(result);
  });
  return false;
}

function unfollow_profile(profile) {
  fetch(`/update/${profile.username}`, {
    method: "DELETE",
  }).then((result) => {
    display_profile(profile.username);
    console.log(result);
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
  if (profile.isOwnProfile) {
    document.querySelector("#profile-follow").innerHTML = "";
  } else {
    const element = document.createElement("div");
    element.innerHTML = `<div class="action-buttons">
    <button class="btn btn-primary" id="followButtons">${
      profile.isFollowing ? "Unfollow" : "Follow"
    }</button>  </div>`;

    document.querySelector("#profile-follow").append(element);

    document
      .querySelector("#followButtons")
      .addEventListener("click", function () {
        check_follow(profile);
      });
  }
}
