using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace KahootPlayer
{
    [Activity(Label = "Register")]
    public class Register : Activity
    {
        Button btnRegReg;
        EditText etRegUname, etRegPword, etRegPwordRep;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Register);
            // Create your application here

            etRegUname = FindViewById<EditText>(Resource.Id.etRegUname);
            etRegPword = FindViewById<EditText>(Resource.Id.etRegPword);
            etRegPwordRep = FindViewById<EditText>(Resource.Id.etRegPwordRep);
            btnRegReg = FindViewById<Button>(Resource.Id.btnRegReg);

            btnRegReg.Click += BtnRegReg_Click;
        }

        private void BtnRegReg_Click(object sender, EventArgs e)
        {
            if (etRegUname.Text.Length > 0 && etRegPword.Text.Length > 0 && etRegPword.Text == etRegPwordRep.Text)
            {
                string data = "#REG#" + etRegUname.Text + "#" + etRegPword.Text;
                string lendata = data.Length.ToString().PadLeft(5, '0') + data;
                Client.Send(lendata);

                string status = Client.Recv();
                string[] msg = status.Split("#");
                status = msg[1];
                if (status == "IN")
                {
                    Intent intent = new Intent(this, typeof(PIN)); 
                    intent.PutExtra("UName", etRegUname.Text);
                    intent.SetFlags(ActivityFlags.NewTask);
                    StartActivity(intent);
                    this.Finish();
                }
                else if (status == "TKN")
                {
                    Toast.MakeText(this, "Username already taken", ToastLength.Long).Show();
                    etRegUname.Text = "";
                    etRegPword.Text = "";
                    etRegPwordRep.Text = "";
                }
            }
        }
    }
}