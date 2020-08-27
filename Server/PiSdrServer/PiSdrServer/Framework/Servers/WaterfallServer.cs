using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace PiSdrServer.Framework.Servers
{
    public class WaterfallServer : BaseServerUDP
    {
        public WaterfallServer() : base(ServerStatics.PORT_WATERFALL)
        {
        }

        private DateTime lastSent;
        private FileStream test = new FileStream("E:\\test", FileMode.Create);

        public override void OnDataReceived(byte[] content)
        {
            if((DateTime.UtcNow - lastSent).TotalMilliseconds > 20)
            {
                Program.waterfallSocks.SendBinary(content);
                lastSent = DateTime.UtcNow;
                test.Write(content, 0, content.Length);
            }
        }
    }
}
