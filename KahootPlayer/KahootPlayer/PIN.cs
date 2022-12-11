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
    [Activity(Label = "PIN")]
    public class PIN : Activity
    {
        EditText etGamePIN;
        Button btnPIN;
        String UName;
        TextView txtPoints;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.PIN);
            // Create your application here
            UName = Intent.GetStringExtra("UName") ?? "not availabe";
            etGamePIN = FindViewById<EditText>(Resource.Id.etGamePIN);
            btnPIN = FindViewById<Button>(Resource.Id.btnPIN);
            txtPoints = FindViewById<TextView>(Resource.Id.txtPoints);
            
            btnPIN.Click += BtnPIN_Click;

            string data = "#GPOINTS#" + UName;
            string lendata = data.Length.ToString().PadLeft(5, '0') + data;
            Client.Send(lendata);

            string status = Client.Recv();
            string[] msg = status.Split("#");
            txtPoints.Text = UName + ", your total points are: " + msg[2];
        }

        private void BtnPIN_Click(object sender, EventArgs e)
        {
            if (etGamePIN.Length() > 0)
            {
                string data = "#PIN#" + etGamePIN.Text;
                string lendata = data.Length.ToString().PadLeft(5, '0') + data;
                Client.Send(lendata);

                string status = Client.Recv();
                string[] msg = status.Split("#");
                status = msg[1];

                if (status == "CONNECT")
                {
                    //Client.Disconnect();
                    Intent intent = new Intent(this, typeof(Waiting));
                    intent.PutExtra("GameIP", msg[2]);
                    intent.PutExtra("UName", UName);
                    intent.SetFlags(ActivityFlags.NewTask);
                    StartActivity(intent);
                    this.Finish();
                }
                else if (status == "WRNG")
                {
                    Toast.MakeText(this, "Wrong Game PIN", ToastLength.Long).Show();
                    etGamePIN.Text = "";
                }
            }
        }
    }
}