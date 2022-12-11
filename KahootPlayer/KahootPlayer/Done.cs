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
    [Activity(Label = "Done")]
    public class Done : Activity
    {
        string UName;
        TextView tvDisplay;
        Button btnPlay, btnClose;
        string IP = "172.20.10.6";
        int PORT = 5000;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Done);
            // Create your application here
            Client.Disconnect();
            Client.Connect(IP, PORT);
            UName = Intent.GetStringExtra("UName") ?? "not available";
            string Points = Intent.GetStringExtra("Points") ?? "not available";

            btnPlay = FindViewById<Button>(Resource.Id.btnPlay);
            btnClose = FindViewById<Button>(Resource.Id.btnClose);
            tvDisplay = FindViewById<TextView>(Resource.Id.tvDisplay);

            tvDisplay.Text = "Game is over, " + UName + ", you received " + Points + " points from this game!";
            btnPlay.Click += BtnPlay_Click;
            btnClose.Click += BtnClose_Click;
        }

        private void BtnClose_Click(object sender, EventArgs e)
        {
            Finish();
        }

        private void BtnPlay_Click(object sender, EventArgs e)
        {
            Intent intent = new Intent(this, typeof(PIN));
            intent.PutExtra("UName", UName);
            intent.SetFlags(ActivityFlags.NewTask);
            StartActivity(intent);
            this.Finish();
        }
    }
}