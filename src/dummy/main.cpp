#include <boost/log/trivial.hpp>
#include <boost/asio.hpp>

int main()
{
    BOOST_LOG_TRIVIAL(info) << "from boost";
    boost::asio::io_context ctx;
}
