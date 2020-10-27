document.addEventListener('DOMContentLoaded', function() {
    id = [];
    die = [];

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.getElementById('compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', add_email)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(reply1='', reply2='', reply3='') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#inspect').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
        document.querySelector('#compose-recipients').value = reply1;
        document.querySelector('#compose-subject').value = reply2;
        document.querySelector('#compose-body').value = reply3;
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#inspect').style.display = 'none';

  // Show the mailbox name
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        console.log(emails);
        emails.toString();
    document.querySelector('#emails-view').innerHTML = `<h2> ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h2>`;
   for(i = 0; i < emails.length; i++)
   {
    if (emails[i]["read"])
    {

        background = "gray";
    }
    else
    {
        background = "white";
    }
    console.log(background)
   document.querySelector('#emails-view').innerHTML += `<div id="email" style="border:solid; background-color:${background};">

   <h1>Email ${i}
    <h3>Subject</h3>
    <p>${emails[i]["subject"]}</p>
    <h3>Recipients</h3>
    <p>${emails[i]["recipients"]}</p>
    <h3>Time Received</h3>
    <p>${emails[i]["timestamp"]}</p>
    <button id=${emails[i]["id"]} type='click'  style="background-color:${background};">View</button>
    </div>`;
}
    // this some ***REMOVED***ing bullshtit ***REMOVED*** bruh it only passes first one then like nah none others work even though they are valid ids = no erroro  and yeah
    for (y=0;y<emails.length;y++)
    {
        die.push(JSON.parse(JSON.stringify(emails[y]["id"])));

    }
    j = 0;
    emails.forEach(function(em)
    {
        console.log(em);
        wow = em["id"]
        document.getElementById(`${wow}`).addEventListener('click', () => view_email(JSON.parse(JSON.stringify(em["id"]))));
        console.log(die);
        j++;
    });





    // ... do something else with emails ..;



})
}

function get_num(emails, wow, y) {
for (j=0;j<emails.length;j++)
    {
        if (j === y)
        {
            return emails[j]["id"];
        }
    }



}

function add_email() {

        rec = document.querySelector('#compose-recipients').value;
        sub = document.querySelector('#compose-subject').value;
         bod = document.querySelector('#compose-body').value;
       fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: rec.toString(),
          subject: sub.toString(),
          body: bod.toString()
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    load_mailbox('sent');


}

function view_email(id)
{


  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#inspect').style.display = 'block';

  console.log(id)

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
    // Print email
    console.log(email);
    if (email["archived"])
    {
        archived = "Remove From Archive";
        opposite = false;
    }
    else
    {
        archived = "Archive";
        opposite = true;
    }



    document.querySelector('#inspect').innerHTML = `

    <h1>Subject</h1>
    <p>${email["subject"]}</p>
    <h3>Recipients</h3>
    <p>${email["recipients"]}</p>
    <h3>Time Received</h3>
    <p>${email["timestamp"]}</p>
    <h3>Message</h3>
    <p>${email["body"]}</p>
    <button id="button" type="click">${archived}</button>
    <button id="rep" type="click">Reply</button>`;

    document.getElementById("button").addEventListener("click", function() {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
          archived : opposite
  })
})
load_mailbox("inbox");
    } );

        if (email["subject"][0] === "R" && email["subject"][1] === "e" )
        {
            Re = ''
        }
        else
        {
        Re = 'Re: '
        }
        document.getElementById("rep").addEventListener("click", () => compose_email(reply1=email["sender"], reply2=`${Re}${email["subject"]}`, reply3=`On ${email["timestamp"]}, ${email["sender"]} wrote: ${email["body"]}`));
    });



    // ... do something else with email ...

fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
      read : true
  })
})
}