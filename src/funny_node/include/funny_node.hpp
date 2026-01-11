#include <cstdint>
#include "custom_types.hpp"
#include "std_types.hpp"
#include "dds_node.hpp"

class FunnyNode : public DDSNode {
public:
    FunnyNode(int32_t funny_number);
    int32_t compute_funny_value(int32_t input_value);
private:
    Voltage voltage_;
    Int32 funny_number_;
};