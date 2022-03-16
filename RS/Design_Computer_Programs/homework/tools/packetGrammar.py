from Design_Computer_Programs.tools.MathLanguage import *
# from Design_Computer_Programs.homework.tools.unparse import Unparser
PACKETGRAMMAR = grammar("""
packet     => _G. packetType packetName [=] BasePacket:New[(] PacketID. pakidname [)] semi?
semi?      => [.;] | ()
packetType => CG | GC
packetName => name
pakidname  => name
fullvar    => prefixexp var
write      => index = self:Write writeType args semi?
read       => index, fullvar = self:Read readType args semi?
args      =>  [(] explist1 [)] | [(] [)] | string
var       => name [[] exp []] | name
prefixexp  => name [.] prefixexp | ()
writeType  => name
readType   => name

writeorreadlist  => write writeorreadlist | read writeorreadlist | write | read
repetition => for var = explist23 
explist1   => exp , explist1 | exp 
explist23  => exp , exp , exp | exp , exp 

statlist   => stat statlist | stat

conds      => cond eliflist else statlist | cond eliflist | cond
cond       => [(] exp [)] then statlist | exp then statlist
stat       => if conds end | repetition do statlist end | writeorreadlist

exp        => preexplist remindexp | remindexp
remindexp  => arg
arg        => nil | true | false | string | number | fullvar 
preexplist => preexp preexplist | preexp
preexp     => arg opt 
opt        =>  and | or | <= | < | >= | > | == | ~= | [-+*/%] 


eliflist   => elseif cond eliflist | () 

laststat   => break
laststat   => return
laststat   => return explist1

uselesslist => useless uselesslist | useless
useless    => ((?!index\\s?[=])(?!index,(?!\\s?size))(?!_G)(?!if)(?!for).)+

file       => ?uselesslist packet uselesslist writeorreadlist ?uselesslist ?statlist ?writeorreadlist ?uselesslist
?uselesslist => uselesslist | ()
?repetition  => repetition | ()
?statlist    => statlist | ()
?writeorreadlist   => writeorreadlist | ()

string     => "[^"]*"
name       => [a-zA-Z_][a-zA-Z0-9_]*
number     => int frac | int
int => -?\d[0-9]*
frac => [.][0-9]+
""")

fail = (None, None)

packet = "_G.CGUseItem = BasePacket:New(PacketID.PACKET_CG_USEITEM);"
write = "index = self:WriteUInt64(l, h, stream, index, size)"
fortest = """for i = 0, self.m_count-1 do
        index = self:WriteByte(self.m_ItemIndex[i], stream, index, size);
        index = self:WriteINT32(self.m_ItemIndex[i], stream, index, size);
    end"""
iftest = """if CGAskCaptainBookOpt.nOptType >= 5 and CGAskCaptainBookOpt.nOptType <= 4 then
                index = self:WriteInt32(CGAskCaptainBookOpt.nBookEventID, stream, index, size)
            elseif CGAskCaptainBookOpt.nOptType == 3 then
                index = self:WriteInt32(CGAskCaptainBookOpt.nBookEventID, stream, index, size)
            end"""

useless = """
    _G.GCPickUpPackage = BasePacket:New(PacketID.PACKET_GC_PACKUP_PACKET);

GCPickUpPackage.m_nResult = 0; -- int

function GCPickUpPackage:GetSize()
    return 1 + 1 + 1 + 1;
end

function GCPickUpPackage:ReadStream(stream, index, size)
    ------------------------以下协议解析过程
    print("----------------GCPickUpPackage:ReadStream-------------------------size = " .. size);

    index, self.m_nResult = self:ReadInt32(stream, index, size);

    return index;
end

--[Comment]
--处理完毕
function GCPickUpPackage:Execute()
    --第二个参数没有意义
    LuaBagManager.bIsArranging = false;
    --if (ChangeEquipManager.Instance != null)
    --    ChangeEquipManager.Instance.onPickUpCompleted ();
    --Debug.Log(Time.realtimeSinceStartup);
    --CEventSender.SendEvent(LuaEvent.ShowPublicTip, Util.LangUtil.GetKey(60273));
    EventSender.SendEvent(LuaEvent.TidyBag,1);
end

function GCPickUpPackage:Clear()
    GCPickUpPackage.m_nResult = 0; -- int
end
"""

useless_test = """
---
--- Generated by EmmyLua(https://github.com/EmmyLua)
--- Created by shenxiaowei.
--- DateTime: 2019/5/20 5:20
---
--- 招募界面 基本信息
_G.GCRetRecruitInfo = BasePacket:New( PacketID.PACKET_GC_RET_RECRUIT_INFO );

GCRetRecruitInfo.RewardData = nil;

local m_nRecruitType    = 0;
local m_nResult         = 0;    -- 1：成功；2：失败
local m_nRewardLen      = 0;
local m_nRewardList     = nil
local openRecruitAnimPanel = false;

function GCRetRecruitInfo:GetSize()
    return 0;
end

function GCRetRecruitInfo:ReadStream( stream, index, size )

    index, m_nRecruitType                   = self:ReadInt32( stream, index, size );
    index, m_nResult                        = self:ReadInt32( stream, index, size );
    index, m_nRewardLen                     = self:ReadInt32( stream, index, size );

    for i = 1, m_nRewardLen do

        index, rewardData.m_nID = self:ReadInt32( stream, index, size );
        index, rewardData.m_nType = self:ReadInt32( stream, index, size );
        index, rewardData.m_nCount = self:ReadInt32( stream, index, size );
        if( rewardData.m_nType == 0 )then
            index, decomposeItemData.m_nID = self:ReadInt32( stream, index, size );
        else

            index, rewardData.m_nDecomposeItemCount = self:ReadInt32( stream, index, size );

            for i = 1, rewardData.m_nDecomposeItemCount do

                index, decomposeItemData.m_nID = self:ReadInt32( stream, index, size );
                index, decomposeItemData.m_nCount = self:ReadInt32( stream, index, size );

            end
        end
    end
    return index;
end

function GCRetRecruitInfo:Execute()
    if( m_nResult == 2 )then
        if(NavigatorRecruitCompassUI:IsOpen())then
            NavigatorRecruitCompassUI:OnClose()
        end
        if NavigatorRecruitMainUI:IsOpen() then
            NavigatorRecruitMainUI:SetCutBlackActive( false );
        end
        NavigatorRecruitMainUI:SetNoticeActive( true );
        NavigatorRecruitMainUI:ActiveRecruitButton(false);
        EventSender.SendEvent( LuaEvent.ShowPublicTip, lang( 219218 ) );
        return;
    end

    GCRetRecruitInfo.RewardData = {};
    GCRetRecruitInfo.RewardData.recruitType = m_nRecruitType;
    GCRetRecruitInfo.RewardData.result = m_nResult;
    GCRetRecruitInfo.RewardData.rewardLen = m_nRewardLen;
    GCRetRecruitInfo.RewardData.rewardList = m_nRewardList;
    GCRetRecruitInfo.RewardData.isShowShanbai = false;
    -- 普通招募：直接弹结果  高级招募：如果结果没有航海士，直接弹结果。否则走罗盘动画
    if( m_nRecruitType == 1 or not openRecruitAnimPanel)then
    --if(  not openRecruitAnimPanel )then
        --普通招募
        NavigatorRecruitCompassUI:OpenSelf(true);
    else
        --其他招募
        Invoke:DelayCall( function()
            RecruitAnimationCoverPanelUI:OpenPanel();
            --RecruitAnimationPanelUI:OpenPanel();
        end, 0.6 );
    end
    EventSender.SendEvent(LuaEvent.RefreshNavigatorPanel)
end

function GCRetRecruitInfo:Clear()
    m_nRecruitType                   = 0;
    m_nResult                         = 0;
    m_nRewardLen                     = 0;
    m_nRewardList                    = nil;
end
"""
# print(parse('packet', packet, PACKETGRAMMAR))
# print(parse('write', write, PACKETGRAMMAR))
# print(parse('stat', fortest, PACKETGRAMMAR))
# print(parse('stat', iftest, PACKETGRAMMAR))

# tree = parse('file', useless_test, PACKETGRAMMAR)
# print(tree)
#
# Unparser(tree[0]) # , 'E:\\tick\\RS\\Design_Computer_Programs\\homework\\tools'