using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace MainPortal
{
    public class Rating
    {
        public string Id { get; set; }
        public string UserId { get; set; }
        public string BookId { get; set; }
        public string Rate { get; set; }
    }
}