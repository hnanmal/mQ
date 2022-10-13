using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ExtendingInterface
{
    public interface IDataSource
    {
        IEnumerable<DataItem> GetItems();
    }
}