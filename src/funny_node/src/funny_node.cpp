#include "funny_node.hpp"

FunnyNode::FunnyNode(int32_t funny_number) : DDSNode("chochacho", 11) {
    voltage_.set_voltage(5.0);
    funny_number_.set_int(funny_number);
}

int32_t FunnyNode::compute_funny_value(int32_t input_value) {
    // A simple computation combining voltage and funny number
    int32_t voltage_component = static_cast<int32_t>(voltage_.get_voltage() * 10);
    int32_t funny_component = funny_number_.get_int();
    return input_value + voltage_component + funny_component;
}