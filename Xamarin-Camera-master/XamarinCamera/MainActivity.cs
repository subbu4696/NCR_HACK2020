using Android.App;
using Android.OS;
using Android.Support.V7.App;
using Android.Runtime;
using Android.Widget;
using Android;
using Plugin.Media;
using Android.Graphics;
using System.Net;
using Android.Media;
using System.Text;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace XamarinCamera
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        Button captureButton;
        Button uploadButton;
        ImageView thisImageView;
        TextView textView1;
        TextView textViewQ;


        readonly string[] permissionGroup =
        {
            Manifest.Permission.ReadExternalStorage,
            Manifest.Permission.WriteExternalStorage,
            Manifest.Permission.Camera
        };

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);

            captureButton = (Button)FindViewById(Resource.Id.captureButton);
            uploadButton = (Button)FindViewById(Resource.Id.uploadButton);
            thisImageView = (ImageView)FindViewById(Resource.Id.thisImageView);

            captureButton.Click += CaptureButton_Click;
            uploadButton.Click += UploadButton_Click;
            RequestPermissions(permissionGroup, 0);
        }

        private void UploadButton_Click(object sender, System.EventArgs e)
        {
            UploadPhoto();
        }

        private void CaptureButton_Click(object sender, System.EventArgs e)
        {
            TakePhoto();
        }

        async void TakePhoto()
        {
            await CrossMedia.Current.Initialize();

            var file = await CrossMedia.Current.TakePhotoAsync(new Plugin.Media.Abstractions.StoreCameraMediaOptions
            {
                PhotoSize = Plugin.Media.Abstractions.PhotoSize.Medium,
                CompressionQuality = 40,
                Name = "myimage.jpg",
                Directory = "sample"
            
            });

            if(file == null)
            {
                return;
            }

            // Convert file to byte array and set the resulting bitmap to imageview
            byte[] imageArray = System.IO.File.ReadAllBytes(file.Path);
            Bitmap bitmap = BitmapFactory.DecodeByteArray(imageArray, 0, imageArray.Length);
            thisImageView.SetImageBitmap(bitmap);
            
            string url = "http://168.61.53.94:5000/cart";

            using (var wb = new WebClient())
            {
                var data = "sample";
                var response = wb.UploadData(url, "POST",imageArray );
                //string responsestring = Encoding.ASCII.GetString(response);
                var jsn = System.Text.Encoding.UTF8.GetString(response);
                var values = JsonConvert.DeserializeObject<Dictionary<string, string>>(jsn);
                textView1 = (TextView)FindViewById(Resource.Id.textView1);
                textView1.Text = values["cartsize"];

                textViewQ = (TextView)FindViewById(Resource.Id.textView3);
                textViewQ.Text = values["Queue"];




            }


        }

        async void UploadPhoto()
        {
            await CrossMedia.Current.Initialize();

            if (!CrossMedia.Current.IsPickPhotoSupported)
            {
                Toast.MakeText(this, "Upload not supported on this device", ToastLength.Short).Show();
                return;
            }

            var file = await CrossMedia.Current.PickPhotoAsync(new Plugin.Media.Abstractions.PickMediaOptions
            {
                PhotoSize = Plugin.Media.Abstractions.PhotoSize.Full,
                CompressionQuality = 40
           
            });

            // Convert file to byre array, to bitmap and set it to our ImageView

            byte[] imageArray = System.IO.File.ReadAllBytes(file.Path);
            Bitmap bitmap = BitmapFactory.DecodeByteArray(imageArray, 0, imageArray.Length);
            thisImageView.SetImageBitmap(bitmap);

            string url = "http://168.61.53.94:5000/cart";

            using (var wb = new WebClient())
            {
                var data = "sample";
                var response = wb.UploadData(url, "POST", imageArray);
                //string responsestring = Encoding.ASCII.GetString(response);
                var jsn = System.Text.Encoding.UTF8.GetString(response);
                var values = JsonConvert.DeserializeObject<Dictionary<string, string>>(jsn);
                textView1 = (TextView)FindViewById(Resource.Id.textView1);
                textView1.Text = values["cartsize"];

                textViewQ = (TextView)FindViewById(Resource.Id.textView3);
                textViewQ.Text = "AllocatedQueue:"+values["Queue"];

            }

        }

        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, Android.Content.PM.Permission[] grantResults)
        {
            Plugin.Permissions.PermissionsImplementation.Current.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}