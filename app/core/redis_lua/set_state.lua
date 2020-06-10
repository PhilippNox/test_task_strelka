redis.call("hset", KEYS[1], 'state', KEYS[2])
return 0

-- redis-cli --ldb --eval set_state.lua
-- redis-cli --eval set_state.lua
--[[ input:
            KEYS[1] - chat_id
            KEYS[2] - state_value
--]]
--[[ output:
             0 - success
--]]