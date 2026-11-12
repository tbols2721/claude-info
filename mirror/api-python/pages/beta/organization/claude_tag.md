---
title: Claude Tag
url: https://platform.claude.com/docs/en/api/python/beta/organization/claude_tag
---

# Claude Tag

## Domain types

### Beta API Key Scope Missing Error Details

- `class BetaAPIKeyScopeMissingErrorDetails`

  The API key lacks the scope the request needs: `read:claude_tag` for a read, `write:claude_tag` for a change.

  - `error_code: Literal["api_key_scope_missing"]`

### Beta Claude Tag Default Setting Source

- `class BetaClaudeTagDefaultSettingSource`

  No settings level sets a value, and the built-in default applies.

  - `type: Literal["default"]`

### Beta Claude Tag Guest Policy

- `type BetaClaudeTagGuestPolicy = ...`

  What Claude does in a channel while a Slack guest is in it, for everyone in the channel. It changes nothing in a channel without Slack guests. More types can be added.

  - `class BetaClaudeTagGuestPolicyAllow`

    Claude answers in the channel.

    - `type: Literal["allow"]`

  - `class BetaClaudeTagGuestPolicyRestrict`

    Claude does not answer in the channel.

    - `type: Literal["restrict"]`

  - `class BetaClaudeTagGuestPolicyChannelOnly`

    Claude answers with only the Bundles attached to the channel itself.

    - `type: Literal["channel_only"]`

### Beta Claude Tag Guest Policy Allow

- `class BetaClaudeTagGuestPolicyAllow`

  Claude answers in the channel.

  - `type: Literal["allow"]`

### Beta Claude Tag Guest Policy Channel Only

- `class BetaClaudeTagGuestPolicyChannelOnly`

  Claude answers with only the Bundles attached to the channel itself.

  - `type: Literal["channel_only"]`

### Beta Claude Tag Guest Policy Restrict

- `class BetaClaudeTagGuestPolicyRestrict`

  Claude does not answer in the channel.

  - `type: Literal["restrict"]`

### Beta Claude Tag Reply Mode

- `type BetaClaudeTagReplyMode = ...`

  How Claude takes part in a Slack channel. A channel alone stores one. More types can be added.

  - `class BetaClaudeTagReplyModeAutomatic`

    Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

    - `type: Literal["automatic"]`

  - `class BetaClaudeTagReplyModeMentionOnly`

    Claude replies only when it is @-mentioned.

    - `type: Literal["mention_only"]`

  - `class BetaClaudeTagReplyModeAlwaysAwake`

    Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

    - `type: Literal["always_awake"]`

  - `class BetaClaudeTagReplyModeThread`

    Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

    - `type: Literal["thread"]`

### Beta Claude Tag Reply Mode Always Awake

- `class BetaClaudeTagReplyModeAlwaysAwake`

  Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

  - `type: Literal["always_awake"]`

### Beta Claude Tag Reply Mode Automatic

- `class BetaClaudeTagReplyModeAutomatic`

  Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

  - `type: Literal["automatic"]`

### Beta Claude Tag Reply Mode Mention Only

- `class BetaClaudeTagReplyModeMentionOnly`

  Claude replies only when it is @-mentioned.

  - `type: Literal["mention_only"]`

### Beta Claude Tag Reply Mode Thread

- `class BetaClaudeTagReplyModeThread`

  Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

  - `type: Literal["thread"]`

### Beta Claude Tag Setting Source

- `type BetaClaudeTagSettingSource = ...`

  The settings level a value comes from. More types can be added.

  - `class BetaClaudeTagSlackChannelSettingSource`

    The value comes from the addressed Slack channel itself.

    - `type: Literal["slack_channel"]`

    - `slack_channel_id: str`

      The channel's identifier, starting with `slch_`.

  - `class BetaClaudeTagSlackWorkspaceSettingSource`

    The value comes from a Slack workspace of the organization.

    - `type: Literal["slack_workspace"]`

    - `slack_workspace_id: str`

      The workspace's identifier, starting with `slws_`.

  - `class BetaClaudeTagSlackParentChannelSettingSource`

    The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

    - `type: Literal["slack_parent_channel"]`

    - `slack_channel_id: str`

      The parent channel's identifier, starting with `slch_`.

  - `class BetaClaudeTagSlackDefaultSettingSource`

    The value comes from the organization's Slack defaults, which have no identifier.

    - `type: Literal["slack_default"]`

  - `class BetaClaudeTagDefaultSettingSource`

    No settings level sets a value, and the built-in default applies.

    - `type: Literal["default"]`

  - `class BetaClaudeTagSlackGridChannelSettingSource`

    The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `type: Literal["slack_grid_channel"]`

    - `slack: BetaClaudeTagSlackChannelIdentifiers`

      Slack's own identifiers for the channel under that other workspace.

      - `channel_id: str`

        Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

        minLength: 2, maxLength: 32

      - `workspace_id: str`

        Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

        minLength: 2, maxLength: 32

### Beta Claude Tag Setting Sources

- `class BetaClaudeTagSettingSources`

  For each setting, the settings level its value in `settings` comes from. Without `include_inherited`, a setting the channel or workspace stores has a source that names the channel or workspace itself, and one it does not store has null, or an empty list for `instructions`. With `include_inherited=true` no member is null: a value that no settings level sets has the source `default`.

  - `enabled: Optional[BetaClaudeTagSettingSource]`

    The settings level `enabled` comes from.

    - `class BetaClaudeTagSlackChannelSettingSource`

      The value comes from the addressed Slack channel itself.

      - `type: Literal["slack_channel"]`

      - `slack_channel_id: str`

        The channel's identifier, starting with `slch_`.

    - `class BetaClaudeTagSlackWorkspaceSettingSource`

      The value comes from a Slack workspace of the organization.

      - `type: Literal["slack_workspace"]`

      - `slack_workspace_id: str`

        The workspace's identifier, starting with `slws_`.

    - `class BetaClaudeTagSlackParentChannelSettingSource`

      The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `type: Literal["slack_parent_channel"]`

      - `slack_channel_id: str`

        The parent channel's identifier, starting with `slch_`.

    - `class BetaClaudeTagSlackDefaultSettingSource`

      The value comes from the organization's Slack defaults, which have no identifier.

      - `type: Literal["slack_default"]`

    - `class BetaClaudeTagDefaultSettingSource`

      No settings level sets a value, and the built-in default applies.

      - `type: Literal["default"]`

    - `class BetaClaudeTagSlackGridChannelSettingSource`

      The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

      - `type: Literal["slack_grid_channel"]`

      - `slack: BetaClaudeTagSlackChannelIdentifiers`

        Slack's own identifiers for the channel under that other workspace.

        - `channel_id: str`

          Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

          minLength: 2, maxLength: 32

        - `workspace_id: str`

          Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

          minLength: 2, maxLength: 32

  - `environment_id: Optional[BetaClaudeTagSettingSource]`

    The settings level `environment_id` comes from.

  - `guest_policy: Optional[BetaClaudeTagSettingSource]`

    The settings level `guest_policy` comes from.

  - `instructions: List[BetaClaudeTagSettingSource]`

    Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

    - `class BetaClaudeTagSlackChannelSettingSource`

      The value comes from the addressed Slack channel itself.

    - `class BetaClaudeTagSlackWorkspaceSettingSource`

      The value comes from a Slack workspace of the organization.

    - `class BetaClaudeTagSlackParentChannelSettingSource`

      The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

    - `class BetaClaudeTagSlackDefaultSettingSource`

      The value comes from the organization's Slack defaults, which have no identifier.

    - `class BetaClaudeTagDefaultSettingSource`

      No settings level sets a value, and the built-in default applies.

    - `class BetaClaudeTagSlackGridChannelSettingSource`

      The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

  - `model: Optional[BetaClaudeTagSettingSource]`

    The settings level `model` comes from.

  - `reply_mode: Optional[BetaClaudeTagSettingSource]`

    The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

### Beta Claude Tag Settings

- `class BetaClaudeTagSettings`

  Claude Tag settings. Without `include_inherited`, a setting that is null is not set on the settings level and is inherited. With it, `enabled` and `guest_policy` are never null, `instructions`, `model` and `environment_id` are null when no settings level sets them, and `reply_mode` is null unless the channel itself stores one.

  - `enabled: Optional[bool]`

    Whether Claude is on. The nearest settings level that sets it decides.

  - `environment_id: Optional[str]`

    The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

  - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

    What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

    - `class BetaClaudeTagGuestPolicyAllow`

      Claude answers in the channel.

      - `type: Literal["allow"]`

    - `class BetaClaudeTagGuestPolicyRestrict`

      Claude does not answer in the channel.

      - `type: Literal["restrict"]`

    - `class BetaClaudeTagGuestPolicyChannelOnly`

      Claude answers with only the Bundles attached to the channel itself.

      - `type: Literal["channel_only"]`

  - `instructions: Optional[str]`

    Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

  - `model: Optional[str]`

    The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

  - `reply_mode: Optional[BetaClaudeTagReplyMode]`

    How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

    - `class BetaClaudeTagReplyModeAutomatic`

      Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

      - `type: Literal["automatic"]`

    - `class BetaClaudeTagReplyModeMentionOnly`

      Claude replies only when it is @-mentioned.

      - `type: Literal["mention_only"]`

    - `class BetaClaudeTagReplyModeAlwaysAwake`

      Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

      - `type: Literal["always_awake"]`

    - `class BetaClaudeTagReplyModeThread`

      Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

      - `type: Literal["thread"]`

### Beta Claude Tag Settings Create

- `class BetaClaudeTagSettingsCreateParam`

  The settings in a request that sets a Slack channel up. A setting left out is not set. A setting sent as null is cleared.

  - `enabled: Optional[bool]`

    Whether Claude is on. `true` on a channel turns Claude on in it even when its workspace stores `false`. Null clears it.

  - `environment_id: Optional[str]`

    The environment Claude's sessions run in: the identifier of an active environment of the organization, starting with `env_`, or of a self-hosted runner pool of the organization that every member may use, starting with `ccpool_`. Null clears it.

    minLength: 1, maxLength: 64

  - `guest_policy: Optional[BetaClaudeTagGuestPolicyParam]`

    What Claude does in a channel while a Slack guest is in it. Null clears it.

    - `class BetaClaudeTagGuestPolicyAllow`

      Claude answers in the channel.

      - `type: Literal["allow"]`

    - `class BetaClaudeTagGuestPolicyRestrict`

      Claude does not answer in the channel.

      - `type: Literal["restrict"]`

    - `class BetaClaudeTagGuestPolicyChannelOnly`

      Claude answers with only the Bundles attached to the channel itself.

      - `type: Literal["channel_only"]`

  - `instructions: Optional[str]`

    Instructions for Claude, up to 8,192 characters after leading and trailing white space is trimmed. Null or blank text clears them.

  - `model: Optional[str]`

    The model Claude uses: the identifier of a model, or the name of a model line, that the organization is entitled to for Claude Tag. Null clears it.

    minLength: 1, maxLength: 128

  - `reply_mode: Optional[BetaClaudeTagReplyModeParam]`

    How Claude takes part in the channel: `automatic`, `mention_only`, `always_awake` or `thread`. Only a channel takes one: an update of a workspace that sends a value is refused, and one that sends null changes nothing. Null never clears it: sent to a channel that stores none it changes nothing, and sent to a channel that stores one it is refused, because a stored reply mode can be changed but never cleared; a caller that wants Claude's default behavior sends `automatic`.

    - `class BetaClaudeTagReplyModeAutomatic`

      Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

      - `type: Literal["automatic"]`

    - `class BetaClaudeTagReplyModeMentionOnly`

      Claude replies only when it is @-mentioned.

      - `type: Literal["mention_only"]`

    - `class BetaClaudeTagReplyModeAlwaysAwake`

      Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

      - `type: Literal["always_awake"]`

    - `class BetaClaudeTagReplyModeThread`

      Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

      - `type: Literal["thread"]`

### Beta Claude Tag Settings Update

- `class BetaClaudeTagSettingsUpdateParam`

  The settings to change. A setting left out is unchanged. A setting sent as null is cleared, so it is inherited.

  - `enabled: Optional[bool]`

    Whether Claude is on. `true` on a channel turns Claude on in it even when its workspace stores `false`. Null clears it.

  - `environment_id: Optional[str]`

    The environment Claude's sessions run in: the identifier of an active environment of the organization, starting with `env_`, or of a self-hosted runner pool of the organization that every member may use, starting with `ccpool_`. Null clears it.

    minLength: 1, maxLength: 64

  - `guest_policy: Optional[BetaClaudeTagGuestPolicyParam]`

    What Claude does in a channel while a Slack guest is in it. Null clears it.

    - `class BetaClaudeTagGuestPolicyAllow`

      Claude answers in the channel.

      - `type: Literal["allow"]`

    - `class BetaClaudeTagGuestPolicyRestrict`

      Claude does not answer in the channel.

      - `type: Literal["restrict"]`

    - `class BetaClaudeTagGuestPolicyChannelOnly`

      Claude answers with only the Bundles attached to the channel itself.

      - `type: Literal["channel_only"]`

  - `instructions: Optional[str]`

    Instructions for Claude, up to 8,192 characters after leading and trailing white space is trimmed. Null or blank text clears them.

  - `model: Optional[str]`

    The model Claude uses: the identifier of a model, or the name of a model line, that the organization is entitled to for Claude Tag. Null clears it.

    minLength: 1, maxLength: 128

  - `reply_mode: Optional[BetaClaudeTagReplyModeParam]`

    How Claude takes part in the channel: `automatic`, `mention_only`, `always_awake` or `thread`. Only a channel takes one: an update of a workspace that sends a value is refused, and one that sends null changes nothing. Null never clears it: sent to a channel that stores none it changes nothing, and sent to a channel that stores one it is refused, because a stored reply mode can be changed but never cleared; a caller that wants Claude's default behavior sends `automatic`.

    - `class BetaClaudeTagReplyModeAutomatic`

      Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

      - `type: Literal["automatic"]`

    - `class BetaClaudeTagReplyModeMentionOnly`

      Claude replies only when it is @-mentioned.

      - `type: Literal["mention_only"]`

    - `class BetaClaudeTagReplyModeAlwaysAwake`

      Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

      - `type: Literal["always_awake"]`

    - `class BetaClaudeTagReplyModeThread`

      Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

      - `type: Literal["thread"]`

### Beta Claude Tag Slack Channel Identifiers

- `class BetaClaudeTagSlackChannelIdentifiers`

  The identifiers Slack shows for a channel. They are Slack's own, not identifiers of this API.

  - `channel_id: str`

    Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

    minLength: 2, maxLength: 32

  - `workspace_id: str`

    Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

    minLength: 2, maxLength: 32

### Beta Claude Tag Slack Channel Setting Source

- `class BetaClaudeTagSlackChannelSettingSource`

  The value comes from the addressed Slack channel itself.

  - `type: Literal["slack_channel"]`

  - `slack_channel_id: str`

    The channel's identifier, starting with `slch_`.

### Beta Claude Tag Slack Default Setting Source

- `class BetaClaudeTagSlackDefaultSettingSource`

  The value comes from the organization's Slack defaults, which have no identifier.

  - `type: Literal["slack_default"]`

### Beta Claude Tag Slack Grid Channel Setting Source

- `class BetaClaudeTagSlackGridChannelSettingSource`

  The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

  - `type: Literal["slack_grid_channel"]`

  - `slack: BetaClaudeTagSlackChannelIdentifiers`

    Slack's own identifiers for the channel under that other workspace.

    - `channel_id: str`

      Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

      minLength: 2, maxLength: 32

    - `workspace_id: str`

      Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

      minLength: 2, maxLength: 32

### Beta Claude Tag Slack Parent Channel Setting Source

- `class BetaClaudeTagSlackParentChannelSettingSource`

  The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

  - `type: Literal["slack_parent_channel"]`

  - `slack_channel_id: str`

    The parent channel's identifier, starting with `slch_`.

### Beta Claude Tag Slack Workspace Identifiers

- `class BetaClaudeTagSlackWorkspaceIdentifiers`

  The identifier Slack shows for a workspace. It is Slack's own, not an identifier of this API.

  - `workspace_id: str`

    Slack's identifier for the workspace, starting with `T`, such as `T0123ABCD`.

### Beta Claude Tag Slack Workspace Setting Source

- `class BetaClaudeTagSlackWorkspaceSettingSource`

  The value comes from a Slack workspace of the organization.

  - `type: Literal["slack_workspace"]`

  - `slack_workspace_id: str`

    The workspace's identifier, starting with `slws_`.

### Beta Claude Tag Writes Not Enabled Error Details

- `class BetaClaudeTagWritesNotEnabledErrorDetails`

  Changes through the Claude Tag API are not enabled for the organization.

  - `error_code: Literal["claude_tag_writes_not_enabled"]`

### Beta Compliance Configuration Restricted Error Details

- `class BetaComplianceConfigurationRestrictedErrorDetails`

  The organization's compliance configuration does not let Claude Tag store anything new.

  - `error_code: Literal["compliance_configuration_restricted"]`

### Beta Organization Level Scoped API Key Required Error Details

- `class BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails`

  The credential is not a scoped API key that is bound at the organization level.

  - `error_code: Literal["organization_level_scoped_api_key_required"]`

### Beta Slack Channel Set Up Environment Not Found Error Details

- `class BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails`

  `settings.environment_id` names no Environment within the organization's reach, and the request had set the channel up by then. The channel stays set up with every setting unset.

  - `error_code: Literal["slack_channel_set_up_environment_not_found"]`

  - `slack_channel_id: str`

    The identifier of the channel the request set up, starting with `slch_`.

### Beta Slack Channel Set Up Settings Conflict Error Details

- `class BetaSlackChannelSetUpSettingsConflictErrorDetails`

  The request set the channel up, and something else then changed the channel or removed it. Nothing of `settings` was stored.

  - `error_code: Literal["slack_channel_set_up_settings_conflict"]`

    A stable code that names the cause.

  - `slack_channel_id: str`

    The identifier of the channel the request set up, starting with `slch_`.

### Beta Slack Channel Set Up Settings Refused Error Details

- `class BetaSlackChannelSetUpSettingsRefusedErrorDetails`

  The request set the channel up, and `settings` was then refused. The channel stays set up with every setting unset.

  - `error_code: Literal["slack_channel_set_up_settings_refused"]`

    A stable code that names the cause.

  - `slack_channel_id: str`

    The identifier of the channel the request set up, starting with `slch_`.

## Claude Tag › Slack Channels

### Set Up Slack Channel

`beta.organization.claude_tag.slack_channels.create(**kwargs) -> BetaClaudeTagSlackChannel`

**POST** `/v1/organizations/claude_tag/slack_channels`

Set a Slack channel up for Claude Tag and return it with its identifier. If the channel is already set up, whether in claude.ai, by Claude's first use in it or by an earlier request, the existing channel is returned, so the request can be repeated. `settings`, when sent, is applied as an update applies it. Before a channel is set up, Claude's Slack app confirms with Slack that the channel is in the workspace, is not archived and is visible to the app; a channel that fails the confirmation returns 404. Setting the channel up and applying `settings` are two steps: when the second is refused, the response is the refusal, the channel stays set up with every setting unset, and the error's `details.slack_channel_id` holds the channel's identifier.

#### Parameters

- `slack: BetaClaudeTagSlackChannelIdentifiersParam`

  Slack's own identifiers for the channel to set up. The organization must own the workspace.

  - `channel_id: str`

    Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

    minLength: 2, maxLength: 32

  - `workspace_id: str`

    Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

    minLength: 2, maxLength: 32

- `settings: Optional[BetaClaudeTagSettingsCreateParam]`

  Settings to store on the channel, applied as Update Slack Channel applies them.

  - `enabled: Optional[bool]`

    Whether Claude is on. `true` on a channel turns Claude on in it even when its workspace stores `false`. Null clears it.

  - `environment_id: Optional[str]`

    The environment Claude's sessions run in: the identifier of an active environment of the organization, starting with `env_`, or of a self-hosted runner pool of the organization that every member may use, starting with `ccpool_`. Null clears it.

    minLength: 1, maxLength: 64

  - `guest_policy: Optional[BetaClaudeTagGuestPolicyParam]`

    What Claude does in a channel while a Slack guest is in it. Null clears it.

    - `class BetaClaudeTagGuestPolicyAllow`

      Claude answers in the channel.

      - `type: Literal["allow"]`

    - `class BetaClaudeTagGuestPolicyRestrict`

      Claude does not answer in the channel.

      - `type: Literal["restrict"]`

    - `class BetaClaudeTagGuestPolicyChannelOnly`

      Claude answers with only the Bundles attached to the channel itself.

      - `type: Literal["channel_only"]`

  - `instructions: Optional[str]`

    Instructions for Claude, up to 8,192 characters after leading and trailing white space is trimmed. Null or blank text clears them.

  - `model: Optional[str]`

    The model Claude uses: the identifier of a model, or the name of a model line, that the organization is entitled to for Claude Tag. Null clears it.

    minLength: 1, maxLength: 128

  - `reply_mode: Optional[BetaClaudeTagReplyModeParam]`

    How Claude takes part in the channel: `automatic`, `mention_only`, `always_awake` or `thread`. Only a channel takes one: an update of a workspace that sends a value is refused, and one that sends null changes nothing. Null never clears it: sent to a channel that stores none it changes nothing, and sent to a channel that stores one it is refused, because a stored reply mode can be changed but never cleared; a caller that wants Claude's default behavior sends `automatic`.

    - `class BetaClaudeTagReplyModeAutomatic`

      Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

      - `type: Literal["automatic"]`

    - `class BetaClaudeTagReplyModeMentionOnly`

      Claude replies only when it is @-mentioned.

      - `type: Literal["mention_only"]`

    - `class BetaClaudeTagReplyModeAlwaysAwake`

      Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

      - `type: Literal["always_awake"]`

    - `class BetaClaudeTagReplyModeThread`

      Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

      - `type: Literal["thread"]`

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackChannel`

  A Slack channel set up for Claude Tag, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_channel"]`

  - `id: str`

    The channel's identifier. Starts with `slch_`. It does not change for as long as the channel is set up, with one exception: a channel that is not configured can get a new one. A channel that is removed and set up again also has a new one. The old one keeps returning 404; look the channel up by its Slack identifiers for the new one.

  - `created_at: datetime`

    Time the channel was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the channel itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackChannelIdentifiers`

    Slack's own identifiers for the channel.

    - `channel_id: str`

      Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

      minLength: 2, maxLength: 32

    - `workspace_id: str`

      Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

      minLength: 2, maxLength: 32

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the channel last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the channel again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_slack_channel = (
    client.beta.organization.claude_tag.slack_channels.create(
        slack={
            "channel_id": "xx",
            "workspace_id": "xx",
        },
    )
)
print(beta_claude_tag_slack_channel.id)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "settings": {
    "enabled": true,
    "environment_id": "environment_id",
    "guest_policy": {
      "type": "allow"
    },
    "instructions": "instructions",
    "model": "model",
    "reply_mode": {
      "type": "automatic"
    }
  },
  "slack": {
    "channel_id": "xx",
    "workspace_id": "xx"
  },
  "sources": {
    "enabled": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "environment_id": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "guest_policy": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "instructions": [
      {
        "slack_channel_id": "slack_channel_id",
        "type": "slack_channel"
      }
    ],
    "model": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "reply_mode": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    }
  },
  "type": "slack_channel",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

### List Slack Channels

`beta.organization.claude_tag.slack_channels.list(**kwargs) -> SyncPageCursor[BetaClaudeTagSlackChannel]`

**GET** `/v1/organizations/claude_tag/slack_channels`

List the set-up Slack channels of one Slack workspace, newest first by `created_at`. A channel that is not set up is not listed: Slack holds the full list of a workspace's channels. Pass `slack_channel_id` as well to look one channel up by its Slack identifiers: `data` then holds that channel, or is empty when it is not set up, and `limit` and `page` are ignored. A workspace that the organization owns only through a Slack Enterprise Grid returns 404 until it is set up. With `include_inherited=true` each channel's `settings` holds what applies in it, and the request fails with 503 rather than resolve against a settings level that could not be read. A `page` cursor resumes only a request with the same `include_inherited`.

#### Parameters

- `slack_workspace_id: str` (query parameter)

  The Slack workspace whose channels to list: Slack's identifier for it, as in the channel object's `slack.workspace_id`, not the workspace object's `id`.

- `include_inherited: Optional[bool]` (query parameter)

  When `true`, `settings` holds what applies in each channel once the settings levels above it are taken into account, and every member of `sources` names the level a value comes from. When `false` or left out, `settings` holds what each channel itself stores.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page, between 1 and 100. Defaults to 20.

  format: int32

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `slack_channel_id: Optional[str]` (query parameter)

  Slack's identifier for one channel of that workspace, as in the channel object's `slack.channel_id`. It is not the channel object's `id`. With it `data` holds that channel alone, or nothing when the channel is not set up.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackChannel`

  A Slack channel set up for Claude Tag, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_channel"]`

  - `id: str`

    The channel's identifier. Starts with `slch_`. It does not change for as long as the channel is set up, with one exception: a channel that is not configured can get a new one. A channel that is removed and set up again also has a new one. The old one keeps returning 404; look the channel up by its Slack identifiers for the new one.

  - `created_at: datetime`

    Time the channel was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the channel itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackChannelIdentifiers`

    Slack's own identifiers for the channel.

    - `channel_id: str`

      Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

      minLength: 2, maxLength: 32

    - `workspace_id: str`

      Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

      minLength: 2, maxLength: 32

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the channel last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the channel again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.claude_tag.slack_channels.list(
    slack_workspace_id="slack_workspace_id",
)
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "created_at": "2019-12-27T18:11:19.117Z",
      "settings": {
        "enabled": true,
        "environment_id": "environment_id",
        "guest_policy": {
          "type": "allow"
        },
        "instructions": "instructions",
        "model": "model",
        "reply_mode": {
          "type": "automatic"
        }
      },
      "slack": {
        "channel_id": "xx",
        "workspace_id": "xx"
      },
      "sources": {
        "enabled": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "environment_id": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "guest_policy": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "instructions": [
          {
            "slack_channel_id": "slack_channel_id",
            "type": "slack_channel"
          }
        ],
        "model": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "reply_mode": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        }
      },
      "type": "slack_channel",
      "updated_at": "2019-12-27T18:11:19.117Z"
    }
  ],
  "next_page": "next_page"
}
```

### Get Slack Channel

`beta.organization.claude_tag.slack_channels.retrieve(id, **kwargs) -> BetaClaudeTagSlackChannel`

**GET** `/v1/organizations/claude_tag/slack_channels/{id}`

Get one Slack channel and its settings. By default `settings` holds what the channel itself stores: a setting that is null there is not set on the channel and is inherited. With `include_inherited=true`, `settings` holds what applies in the channel once the settings levels above it are taken into account, and the request fails with 503 rather than resolve against a settings level that could not be read. Either way `sources` names the settings level each value comes from, so a caller tells the channel's own value from an inherited one by its source, not by whether it is null.

#### Parameters

- `id: str` (path parameter)

  The channel's identifier, starting with `slch_`.

- `include_inherited: Optional[bool]` (query parameter)

  When `true`, `settings` holds what applies in the channel once the settings levels above it are taken into account, and every member of `sources` names the level a value comes from. When `false` or left out, `settings` holds what the channel itself stores.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackChannel`

  A Slack channel set up for Claude Tag, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_channel"]`

  - `id: str`

    The channel's identifier. Starts with `slch_`. It does not change for as long as the channel is set up, with one exception: a channel that is not configured can get a new one. A channel that is removed and set up again also has a new one. The old one keeps returning 404; look the channel up by its Slack identifiers for the new one.

  - `created_at: datetime`

    Time the channel was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the channel itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackChannelIdentifiers`

    Slack's own identifiers for the channel.

    - `channel_id: str`

      Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

      minLength: 2, maxLength: 32

    - `workspace_id: str`

      Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

      minLength: 2, maxLength: 32

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the channel last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the channel again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_slack_channel = (
    client.beta.organization.claude_tag.slack_channels.retrieve(
        id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
    )
)
print(beta_claude_tag_slack_channel.id)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "settings": {
    "enabled": true,
    "environment_id": "environment_id",
    "guest_policy": {
      "type": "allow"
    },
    "instructions": "instructions",
    "model": "model",
    "reply_mode": {
      "type": "automatic"
    }
  },
  "slack": {
    "channel_id": "xx",
    "workspace_id": "xx"
  },
  "sources": {
    "enabled": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "environment_id": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "guest_policy": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "instructions": [
      {
        "slack_channel_id": "slack_channel_id",
        "type": "slack_channel"
      }
    ],
    "model": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "reply_mode": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    }
  },
  "type": "slack_channel",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

### Update Slack Channel

`beta.organization.claude_tag.slack_channels.update(id, **kwargs) -> BetaClaudeTagSlackChannel`

**POST** `/v1/organizations/claude_tag/slack_channels/{id}`

Change the settings a Slack channel stores. The update is partial: a setting left out is unchanged, and a setting sent as null is cleared, so the channel inherits it. If any value is refused, no setting in the request is stored. A group direct message takes no settings and returns 400.

#### Parameters

- `id: str` (path parameter)

  The channel's identifier, starting with `slch_`.

- `settings: BetaClaudeTagSettingsUpdateParam`

  The settings to change.

  - `enabled: Optional[bool]`

    Whether Claude is on. `true` on a channel turns Claude on in it even when its workspace stores `false`. Null clears it.

  - `environment_id: Optional[str]`

    The environment Claude's sessions run in: the identifier of an active environment of the organization, starting with `env_`, or of a self-hosted runner pool of the organization that every member may use, starting with `ccpool_`. Null clears it.

    minLength: 1, maxLength: 64

  - `guest_policy: Optional[BetaClaudeTagGuestPolicyParam]`

    What Claude does in a channel while a Slack guest is in it. Null clears it.

    - `class BetaClaudeTagGuestPolicyAllow`

      Claude answers in the channel.

      - `type: Literal["allow"]`

    - `class BetaClaudeTagGuestPolicyRestrict`

      Claude does not answer in the channel.

      - `type: Literal["restrict"]`

    - `class BetaClaudeTagGuestPolicyChannelOnly`

      Claude answers with only the Bundles attached to the channel itself.

      - `type: Literal["channel_only"]`

  - `instructions: Optional[str]`

    Instructions for Claude, up to 8,192 characters after leading and trailing white space is trimmed. Null or blank text clears them.

  - `model: Optional[str]`

    The model Claude uses: the identifier of a model, or the name of a model line, that the organization is entitled to for Claude Tag. Null clears it.

    minLength: 1, maxLength: 128

  - `reply_mode: Optional[BetaClaudeTagReplyModeParam]`

    How Claude takes part in the channel: `automatic`, `mention_only`, `always_awake` or `thread`. Only a channel takes one: an update of a workspace that sends a value is refused, and one that sends null changes nothing. Null never clears it: sent to a channel that stores none it changes nothing, and sent to a channel that stores one it is refused, because a stored reply mode can be changed but never cleared; a caller that wants Claude's default behavior sends `automatic`.

    - `class BetaClaudeTagReplyModeAutomatic`

      Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

      - `type: Literal["automatic"]`

    - `class BetaClaudeTagReplyModeMentionOnly`

      Claude replies only when it is @-mentioned.

      - `type: Literal["mention_only"]`

    - `class BetaClaudeTagReplyModeAlwaysAwake`

      Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

      - `type: Literal["always_awake"]`

    - `class BetaClaudeTagReplyModeThread`

      Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

      - `type: Literal["thread"]`

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackChannel`

  A Slack channel set up for Claude Tag, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_channel"]`

  - `id: str`

    The channel's identifier. Starts with `slch_`. It does not change for as long as the channel is set up, with one exception: a channel that is not configured can get a new one. A channel that is removed and set up again also has a new one. The old one keeps returning 404; look the channel up by its Slack identifiers for the new one.

  - `created_at: datetime`

    Time the channel was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the channel itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackChannelIdentifiers`

    Slack's own identifiers for the channel.

    - `channel_id: str`

      Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

      minLength: 2, maxLength: 32

    - `workspace_id: str`

      Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

      minLength: 2, maxLength: 32

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the channel last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the channel again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_slack_channel = (
    client.beta.organization.claude_tag.slack_channels.update(
        id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
        settings={},
    )
)
print(beta_claude_tag_slack_channel.id)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "settings": {
    "enabled": true,
    "environment_id": "environment_id",
    "guest_policy": {
      "type": "allow"
    },
    "instructions": "instructions",
    "model": "model",
    "reply_mode": {
      "type": "automatic"
    }
  },
  "slack": {
    "channel_id": "xx",
    "workspace_id": "xx"
  },
  "sources": {
    "enabled": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "environment_id": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "guest_policy": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "instructions": [
      {
        "slack_channel_id": "slack_channel_id",
        "type": "slack_channel"
      }
    ],
    "model": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "reply_mode": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    }
  },
  "type": "slack_channel",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

### Remove Slack Channel

`beta.organization.claude_tag.slack_channels.delete(id, **kwargs) -> BetaClaudeTagDeletedSlackChannel`

**DELETE** `/v1/organizations/claude_tag/slack_channels/{id}`

Remove a Slack channel from Claude Tag. This deletes the channel's stored settings and its Bundle Targets at once, and then, in the background, the channel's sessions and their transcripts, its memory, its routines and the artifacts published from it. None of it can be restored. The channel in Slack and its messages are unchanged. The request is refused with 400 and `error.details.error_code` `slack_channel_enabled` while `enabled` resolves to `true` for the channel, as a read with `include_inherited=true` returns it: set `enabled` to `false` on the channel first. This guards against removing a channel in use by mistake; it is not a way to keep Claude out, because the removal deletes the channel's own `enabled: false` with its other settings, after which the channel inherits again and Claude's next use of it can set it up anew with a new identifier. The identifier returns 404 as soon as the request returns, so a repeated removal returns 404. A group direct message returns 400, and so does a channel that holds configuration this API does not manage.

#### Parameters

- `id: str` (path parameter)

  The channel's identifier, starting with `slch_`.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagDeletedSlackChannel`

  Confirms that a Slack channel was removed from Claude Tag.

  - `type: Literal["slack_channel_deleted"]`

  - `id: str`

    The removed channel's identifier.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_deleted_slack_channel = (
    client.beta.organization.claude_tag.slack_channels.delete(
        id="slch_01SvpyRQK3nN6eH9uhRA7n1q",
    )
)
print(beta_claude_tag_deleted_slack_channel.id)
```

##### Response (200)

```json
{
  "id": "id",
  "type": "slack_channel_deleted"
}
```

## Claude Tag › Slack Workspaces

### List Slack Workspaces

`beta.organization.claude_tag.slack_workspaces.list(**kwargs) -> SyncPageCursor[BetaClaudeTagSlackWorkspace]`

**GET** `/v1/organizations/claude_tag/slack_workspaces`

List the set-up Slack workspaces the organization owns, newest first by `created_at`. Pass `slack_workspace_id` to look one workspace up by its Slack identifier: `data` then holds that workspace, or is empty when it is not set up. A workspace of a Slack Enterprise Grid the organization has connected returns 404 until it is set up. With `include_inherited=true` each workspace's `settings` holds what applies in it, and the request fails with 503 rather than resolve against a settings level that could not be read. A `page` cursor resumes only a request with the same `include_inherited`.

#### Parameters

- `include_inherited: Optional[bool]` (query parameter)

  When `true`, `settings` holds what applies in each workspace once the organization's Slack defaults are taken into account, and every member of `sources` names the level a value comes from. When `false` or left out, `settings` holds what each workspace itself stores.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page, between 1 and 100. Defaults to 20.

  format: int32

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `slack_workspace_id: Optional[str]` (query parameter)

  Slack's identifier for one workspace, as in the workspace object's `slack.workspace_id`, not its `id`. With it `data` holds that workspace alone, or nothing when it is not set up.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackWorkspace`

  A Slack workspace the organization has connected, itself or through its Slack Enterprise Grid, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_workspace"]`

  - `id: str`

    The workspace's identifier. Starts with `slws_`. It does not change for as long as the workspace is set up. A workspace that is removed and set up again has a new one, and the old one keeps returning 404; look the workspace up by its Slack identifier for the new one.

  - `created_at: datetime`

    Time the workspace was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the workspace itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackWorkspaceIdentifiers`

    Slack's own identifier for the workspace.

    - `workspace_id: str`

      Slack's identifier for the workspace, starting with `T`, such as `T0123ABCD`.

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

          - `channel_id: str`

            Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

            minLength: 2, maxLength: 32

          - `workspace_id: str`

            Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

            minLength: 2, maxLength: 32

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the workspace last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the workspace again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.claude_tag.slack_workspaces.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "created_at": "2019-12-27T18:11:19.117Z",
      "settings": {
        "enabled": true,
        "environment_id": "environment_id",
        "guest_policy": {
          "type": "allow"
        },
        "instructions": "instructions",
        "model": "model",
        "reply_mode": {
          "type": "automatic"
        }
      },
      "slack": {
        "workspace_id": "workspace_id"
      },
      "sources": {
        "enabled": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "environment_id": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "guest_policy": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "instructions": [
          {
            "slack_channel_id": "slack_channel_id",
            "type": "slack_channel"
          }
        ],
        "model": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        },
        "reply_mode": {
          "slack_channel_id": "slack_channel_id",
          "type": "slack_channel"
        }
      },
      "type": "slack_workspace",
      "updated_at": "2019-12-27T18:11:19.117Z"
    }
  ],
  "next_page": "next_page"
}
```

### Get Slack Workspace

`beta.organization.claude_tag.slack_workspaces.retrieve(id, **kwargs) -> BetaClaudeTagSlackWorkspace`

**GET** `/v1/organizations/claude_tag/slack_workspaces/{id}`

Get one Slack workspace and its settings. By default `settings` holds what the workspace itself stores: a setting that is null there is not set on the workspace and is inherited. With `include_inherited=true`, `settings` holds what applies in the workspace once the organization's Slack defaults are taken into account, and the request fails with 503 rather than resolve against a settings level that could not be read. Either way `sources` names the settings level each value comes from.

#### Parameters

- `id: str` (path parameter)

  The workspace's identifier, starting with `slws_`.

- `include_inherited: Optional[bool]` (query parameter)

  When `true`, `settings` holds what applies in the workspace once the organization's Slack defaults are taken into account, and every member of `sources` names the level a value comes from. When `false` or left out, `settings` holds what the workspace itself stores.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackWorkspace`

  A Slack workspace the organization has connected, itself or through its Slack Enterprise Grid, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_workspace"]`

  - `id: str`

    The workspace's identifier. Starts with `slws_`. It does not change for as long as the workspace is set up. A workspace that is removed and set up again has a new one, and the old one keeps returning 404; look the workspace up by its Slack identifier for the new one.

  - `created_at: datetime`

    Time the workspace was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the workspace itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackWorkspaceIdentifiers`

    Slack's own identifier for the workspace.

    - `workspace_id: str`

      Slack's identifier for the workspace, starting with `T`, such as `T0123ABCD`.

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

          - `channel_id: str`

            Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

            minLength: 2, maxLength: 32

          - `workspace_id: str`

            Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

            minLength: 2, maxLength: 32

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the workspace last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the workspace again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_slack_workspace = (
    client.beta.organization.claude_tag.slack_workspaces.retrieve(
        id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
    )
)
print(beta_claude_tag_slack_workspace.id)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "settings": {
    "enabled": true,
    "environment_id": "environment_id",
    "guest_policy": {
      "type": "allow"
    },
    "instructions": "instructions",
    "model": "model",
    "reply_mode": {
      "type": "automatic"
    }
  },
  "slack": {
    "workspace_id": "workspace_id"
  },
  "sources": {
    "enabled": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "environment_id": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "guest_policy": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "instructions": [
      {
        "slack_channel_id": "slack_channel_id",
        "type": "slack_channel"
      }
    ],
    "model": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "reply_mode": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    }
  },
  "type": "slack_workspace",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

### Update Slack Workspace

`beta.organization.claude_tag.slack_workspaces.update(id, **kwargs) -> BetaClaudeTagSlackWorkspace`

**POST** `/v1/organizations/claude_tag/slack_workspaces/{id}`

Change the settings a Slack workspace stores. The update is partial: a setting left out is unchanged, and a setting sent as null is cleared, so the workspace inherits it. If any value is refused, no setting in the request is stored.

#### Parameters

- `id: str` (path parameter)

  The workspace's identifier, starting with `slws_`.

- `settings: BetaClaudeTagSettingsUpdateParam`

  The settings to change.

  - `enabled: Optional[bool]`

    Whether Claude is on. `true` on a channel turns Claude on in it even when its workspace stores `false`. Null clears it.

  - `environment_id: Optional[str]`

    The environment Claude's sessions run in: the identifier of an active environment of the organization, starting with `env_`, or of a self-hosted runner pool of the organization that every member may use, starting with `ccpool_`. Null clears it.

    minLength: 1, maxLength: 64

  - `guest_policy: Optional[BetaClaudeTagGuestPolicyParam]`

    What Claude does in a channel while a Slack guest is in it. Null clears it.

    - `class BetaClaudeTagGuestPolicyAllow`

      Claude answers in the channel.

      - `type: Literal["allow"]`

    - `class BetaClaudeTagGuestPolicyRestrict`

      Claude does not answer in the channel.

      - `type: Literal["restrict"]`

    - `class BetaClaudeTagGuestPolicyChannelOnly`

      Claude answers with only the Bundles attached to the channel itself.

      - `type: Literal["channel_only"]`

  - `instructions: Optional[str]`

    Instructions for Claude, up to 8,192 characters after leading and trailing white space is trimmed. Null or blank text clears them.

  - `model: Optional[str]`

    The model Claude uses: the identifier of a model, or the name of a model line, that the organization is entitled to for Claude Tag. Null clears it.

    minLength: 1, maxLength: 128

  - `reply_mode: Optional[BetaClaudeTagReplyModeParam]`

    How Claude takes part in the channel: `automatic`, `mention_only`, `always_awake` or `thread`. Only a channel takes one: an update of a workspace that sends a value is refused, and one that sends null changes nothing. Null never clears it: sent to a channel that stores none it changes nothing, and sent to a channel that stores one it is refused, because a stored reply mode can be changed but never cleared; a caller that wants Claude's default behavior sends `automatic`.

    - `class BetaClaudeTagReplyModeAutomatic`

      Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

      - `type: Literal["automatic"]`

    - `class BetaClaudeTagReplyModeMentionOnly`

      Claude replies only when it is @-mentioned.

      - `type: Literal["mention_only"]`

    - `class BetaClaudeTagReplyModeAlwaysAwake`

      Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

      - `type: Literal["always_awake"]`

    - `class BetaClaudeTagReplyModeThread`

      Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

      - `type: Literal["thread"]`

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagSlackWorkspace`

  A Slack workspace the organization has connected, itself or through its Slack Enterprise Grid, with the settings it stores or, with `include_inherited`, the settings that apply in it.

  - `type: Literal["slack_workspace"]`

  - `id: str`

    The workspace's identifier. Starts with `slws_`. It does not change for as long as the workspace is set up. A workspace that is removed and set up again has a new one, and the old one keeps returning 404; look the workspace up by its Slack identifier for the new one.

  - `created_at: datetime`

    Time the workspace was set up, by whichever route. It does not change for as long as `id` does not.

    format: date-time

  - `settings: BetaClaudeTagSettings`

    What the workspace itself stores or, with `include_inherited`, what applies in it. `sources` says which.

    - `enabled: Optional[bool]`

      Whether Claude is on. The nearest settings level that sets it decides.

    - `environment_id: Optional[str]`

      The environment Claude's sessions run in, starting with `env_`, or the identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest settings level that sets it decides.

    - `guest_policy: Optional[BetaClaudeTagGuestPolicy]`

      What Claude does in a channel while a Slack guest is in it. The nearest settings level that sets it decides.

      - `class BetaClaudeTagGuestPolicyAllow`

        Claude answers in the channel.

        - `type: Literal["allow"]`

      - `class BetaClaudeTagGuestPolicyRestrict`

        Claude does not answer in the channel.

        - `type: Literal["restrict"]`

      - `class BetaClaudeTagGuestPolicyChannelOnly`

        Claude answers with only the Bundles attached to the channel itself.

        - `type: Literal["channel_only"]`

    - `instructions: Optional[str]`

      Instructions for Claude. Instructions add up: the text of every settings level that sets it is joined, broadest first.

    - `model: Optional[str]`

      The model Claude uses: a model identifier or the name of a model line. The nearest settings level that sets it decides. When none does, Claude uses the product's default model.

    - `reply_mode: Optional[BetaClaudeTagReplyMode]`

      How Claude takes part in the channel. Only a channel stores one, and no settings level passes one on, so it is always null on a workspace. Null on a channel means the channel stores none yet: Claude then follows the reply mode chosen in Slack, if one was, else `automatic`. A stored reply mode can be changed but never cleared.

      - `class BetaClaudeTagReplyModeAutomatic`

        Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.

        - `type: Literal["automatic"]`

      - `class BetaClaudeTagReplyModeMentionOnly`

        Claude replies only when it is @-mentioned.

        - `type: Literal["mention_only"]`

      - `class BetaClaudeTagReplyModeAlwaysAwake`

        Like `automatic`, but Claude never pauses on its own. Available where it is enabled for the channel.

        - `type: Literal["always_awake"]`

      - `class BetaClaudeTagReplyModeThread`

        Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.

        - `type: Literal["thread"]`

  - `slack: BetaClaudeTagSlackWorkspaceIdentifiers`

    Slack's own identifier for the workspace.

    - `workspace_id: str`

      Slack's identifier for the workspace, starting with `T`, such as `T0123ABCD`.

  - `sources: BetaClaudeTagSettingSources`

    For each setting, the settings level its value in `settings` comes from.

    - `enabled: Optional[BetaClaudeTagSettingSource]`

      The settings level `enabled` comes from.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

        - `type: Literal["slack_channel"]`

        - `slack_channel_id: str`

          The channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

        - `type: Literal["slack_workspace"]`

        - `slack_workspace_id: str`

          The workspace's identifier, starting with `slws_`.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

        - `type: Literal["slack_parent_channel"]`

        - `slack_channel_id: str`

          The parent channel's identifier, starting with `slch_`.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

        - `type: Literal["slack_default"]`

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

        - `type: Literal["default"]`

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

        - `type: Literal["slack_grid_channel"]`

        - `slack: BetaClaudeTagSlackChannelIdentifiers`

          Slack's own identifiers for the channel under that other workspace.

          - `channel_id: str`

            Slack's identifier for the channel, starting with `C` or `G`, such as `C0456EFGH`.

            minLength: 2, maxLength: 32

          - `workspace_id: str`

            Slack's identifier for the workspace the channel is in, starting with `T`, such as `T0123ABCD`.

            minLength: 2, maxLength: 32

    - `environment_id: Optional[BetaClaudeTagSettingSource]`

      The settings level `environment_id` comes from.

    - `guest_policy: Optional[BetaClaudeTagSettingSource]`

      The settings level `guest_policy` comes from.

    - `instructions: List[BetaClaudeTagSettingSource]`

      Every settings level that contributes text to `instructions`, broadest first, in the order their text is joined. Empty when none does.

      - `class BetaClaudeTagSlackChannelSettingSource`

        The value comes from the addressed Slack channel itself.

      - `class BetaClaudeTagSlackWorkspaceSettingSource`

        The value comes from a Slack workspace of the organization.

      - `class BetaClaudeTagSlackParentChannelSettingSource`

        The value comes from the channel that a code channel was started from. A parent channel contributes `instructions` and `environment_id` only.

      - `class BetaClaudeTagSlackDefaultSettingSource`

        The value comes from the organization's Slack defaults, which have no identifier.

      - `class BetaClaudeTagDefaultSettingSource`

        No settings level sets a value, and the built-in default applies.

      - `class BetaClaudeTagSlackGridChannelSettingSource`

        The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.

    - `model: Optional[BetaClaudeTagSettingSource]`

      The settings level `model` comes from.

    - `reply_mode: Optional[BetaClaudeTagSettingSource]`

      The settings level `reply_mode` comes from: the channel when it stores one. With `include_inherited=true` and no stored mode it is `default`.

  - `updated_at: datetime`

    Time Claude Tag's record of the workspace last changed. It moves on every change to a setting, and can also move when something no response holds changes, so a later value says to read the workspace again, not that a setting changed. Attaching or detaching a Bundle does not by itself move it.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_slack_workspace = (
    client.beta.organization.claude_tag.slack_workspaces.update(
        id="slws_01Hq8TzW5mKc2YbX7vNd4RfJ",
        settings={},
    )
)
print(beta_claude_tag_slack_workspace.id)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "settings": {
    "enabled": true,
    "environment_id": "environment_id",
    "guest_policy": {
      "type": "allow"
    },
    "instructions": "instructions",
    "model": "model",
    "reply_mode": {
      "type": "automatic"
    }
  },
  "slack": {
    "workspace_id": "workspace_id"
  },
  "sources": {
    "enabled": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "environment_id": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "guest_policy": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "instructions": [
      {
        "slack_channel_id": "slack_channel_id",
        "type": "slack_channel"
      }
    ],
    "model": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    },
    "reply_mode": {
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    }
  },
  "type": "slack_workspace",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

## Claude Tag › Bundles

### List Bundles

`beta.organization.claude_tag.bundles.list(**kwargs) -> SyncPageCursor[BetaClaudeTagBundle]`

**GET** `/v1/organizations/claude_tag/bundles`

List the organization's Bundles, newest first by `created_at`. A Bundle that Claude Tag manages for itself is not listed.

#### Parameters

- `limit: Optional[int]` (query parameter)

  Number of items to return per page, between 1 and 100. Defaults to 20.

  format: int32

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagBundle`

  A named set of access that Claude can use in a Slack channel or a Slack workspace: connectors, repositories and credentials. Created and edited in claude.ai.

  - `type: Literal["bundle"]`

  - `id: str`

    The Bundle's identifier. Starts with `capp_`.

  - `created_at: datetime`

    Time the Bundle was created.

    format: date-time

  - `description: Optional[str]`

    What the Bundle is for. Null when it has none. Read-only.

  - `display_name: str`

    The Bundle's name. Always set. Read-only.

  - `updated_at: datetime`

    Time of the last change to the Bundle.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.claude_tag.bundles.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "created_at": "2019-12-27T18:11:19.117Z",
      "description": "description",
      "display_name": "display_name",
      "type": "bundle",
      "updated_at": "2019-12-27T18:11:19.117Z"
    }
  ],
  "next_page": "next_page"
}
```

### Get Bundle

`beta.organization.claude_tag.bundles.retrieve(bundle_id, **kwargs) -> BetaClaudeTagBundle`

**GET** `/v1/organizations/claude_tag/bundles/{bundle_id}`

Get one Bundle. What the Bundle grants (connectors, repositories and credentials) is never returned.

#### Parameters

- `bundle_id: str` (path parameter)

  The Bundle's identifier, starting with `capp_`.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagBundle`

  A named set of access that Claude can use in a Slack channel or a Slack workspace: connectors, repositories and credentials. Created and edited in claude.ai.

  - `type: Literal["bundle"]`

  - `id: str`

    The Bundle's identifier. Starts with `capp_`.

  - `created_at: datetime`

    Time the Bundle was created.

    format: date-time

  - `description: Optional[str]`

    What the Bundle is for. Null when it has none. Read-only.

  - `display_name: str`

    The Bundle's name. Always set. Read-only.

  - `updated_at: datetime`

    Time of the last change to the Bundle.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_bundle = client.beta.organization.claude_tag.bundles.retrieve(
    bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
)
print(beta_claude_tag_bundle.id)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "description": "description",
  "display_name": "display_name",
  "type": "bundle",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

## Claude Tag › Bundles › Targets

### List Bundle Targets

`beta.organization.claude_tag.bundles.targets.list(bundle_id, **kwargs) -> SyncPageCursor[BetaClaudeTagBundleTarget]`

**GET** `/v1/organizations/claude_tag/bundles/{bundle_id}/targets`

List the Slack channels and Slack workspaces a Bundle is attached to, newest first by `created_at`. Only channels and workspaces the organization owns are listed; a Bundle that is attached to anything else has no Bundle Target for it.

#### Parameters

- `bundle_id: str` (path parameter)

  The Bundle's identifier, starting with `capp_`.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page, between 1 and 100. Defaults to 20.

  format: int32

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `type BetaClaudeTagBundleTarget = ...`

  One Bundle attached to one Slack channel or one Slack workspace. More types of target can be added.

  - `class BetaClaudeTagSlackChannelBundleTarget`

    One Bundle attached to one Slack channel. The Bundle can be used in that channel only.

    - `type: Literal["slack_channel"]`

    - `id: str`

      The Bundle Target's identifier. Starts with `btgt_`. No two Bundle Targets have the same one, and the same Bundle and target always give the same one, also after a detach and a new attach. It is opaque.

    - `created_at: datetime`

      Time the Bundle was attached.

      format: date-time

    - `slack_channel_id: str`

      The identifier of the Slack channel the Bundle is attached to, starting with `slch_`. It is the channel object's `id`, not Slack's `channel_id`.

  - `class BetaClaudeTagSlackWorkspaceBundleTarget`

    One Bundle attached to one Slack workspace. The Bundle can be used in the workspace and in every channel in it.

    - `type: Literal["slack_workspace"]`

    - `id: str`

      The Bundle Target's identifier. Starts with `btgt_`. No two Bundle Targets have the same one, and the same Bundle and target always give the same one, also after a detach and a new attach. It is opaque.

    - `created_at: datetime`

      Time the Bundle was attached.

      format: date-time

    - `slack_workspace_id: str`

      The identifier of the Slack workspace the Bundle is attached to, starting with `slws_`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.claude_tag.bundles.targets.list(
    bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
)
page = page.data[0]
print(page)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "created_at": "2019-12-27T18:11:19.117Z",
      "slack_channel_id": "slack_channel_id",
      "type": "slack_channel"
    }
  ],
  "next_page": "next_page"
}
```

### Attach Bundle

`beta.organization.claude_tag.bundles.targets.create(bundle_id, **kwargs) -> BetaClaudeTagBundleTarget`

**POST** `/v1/organizations/claude_tag/bundles/{bundle_id}/targets`

Attach a Bundle to a Slack channel or a Slack workspace. A Bundle attached to a workspace can be used in the workspace and in every channel in it. Attaching a Bundle to a channel or workspace it is already attached to returns the existing Bundle Target. The channel or workspace must be set up: attaching never sets a channel up. A group direct message takes no Bundle and returns 400.

#### Parameters

- `bundle_id: str` (path parameter)

  The Bundle's identifier, starting with `capp_`.

- `target: BetaClaudeTagBundleTargetCreateParam`

  - `class BetaClaudeTagSlackChannelBundleTargetCreateParam`

    Attach the Bundle to a Slack channel.

    - `type: Literal["slack_channel"]`

    - `slack_channel_id: str`

      The identifier of the Slack channel to attach the Bundle to, starting with `slch_`. It is the channel object's `id`, not Slack's `channel_id`.

      minLength: 8, maxLength: 64

  - `class BetaClaudeTagSlackWorkspaceBundleTargetCreateParam`

    Attach the Bundle to a Slack workspace.

    - `type: Literal["slack_workspace"]`

    - `slack_workspace_id: str`

      The identifier of the Slack workspace to attach the Bundle to, starting with `slws_`.

      minLength: 8, maxLength: 64

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `type BetaClaudeTagBundleTarget = ...`

  One Bundle attached to one Slack channel or one Slack workspace. More types of target can be added.

  - `class BetaClaudeTagSlackChannelBundleTarget`

    One Bundle attached to one Slack channel. The Bundle can be used in that channel only.

    - `type: Literal["slack_channel"]`

    - `id: str`

      The Bundle Target's identifier. Starts with `btgt_`. No two Bundle Targets have the same one, and the same Bundle and target always give the same one, also after a detach and a new attach. It is opaque.

    - `created_at: datetime`

      Time the Bundle was attached.

      format: date-time

    - `slack_channel_id: str`

      The identifier of the Slack channel the Bundle is attached to, starting with `slch_`. It is the channel object's `id`, not Slack's `channel_id`.

  - `class BetaClaudeTagSlackWorkspaceBundleTarget`

    One Bundle attached to one Slack workspace. The Bundle can be used in the workspace and in every channel in it.

    - `type: Literal["slack_workspace"]`

    - `id: str`

      The Bundle Target's identifier. Starts with `btgt_`. No two Bundle Targets have the same one, and the same Bundle and target always give the same one, also after a detach and a new attach. It is opaque.

    - `created_at: datetime`

      Time the Bundle was attached.

      format: date-time

    - `slack_workspace_id: str`

      The identifier of the Slack workspace the Bundle is attached to, starting with `slws_`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_bundle_target = (
    client.beta.organization.claude_tag.bundles.targets.create(
        bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
        target={
            "slack_channel_id": "xxxxxxxx",
            "type": "slack_channel",
        },
    )
)
print(beta_claude_tag_bundle_target)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "slack_channel_id": "slack_channel_id",
  "type": "slack_channel"
}
```

### Get Bundle Target

`beta.organization.claude_tag.bundles.targets.retrieve(target_id, **kwargs) -> BetaClaudeTagBundleTarget`

**GET** `/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}`

Get one Bundle Target. Returns 404 when `target_id` is the identifier of another Bundle's Bundle Target, or the Bundle Target was detached.

#### Parameters

- `bundle_id: str` (path parameter)

  The Bundle's identifier, starting with `capp_`.

- `target_id: str` (path parameter)

  The Bundle Target's identifier, starting with `btgt_`. Attach Bundle and List Bundle Targets return it. It is never the identifier of the channel or workspace.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `type BetaClaudeTagBundleTarget = ...`

  One Bundle attached to one Slack channel or one Slack workspace. More types of target can be added.

  - `class BetaClaudeTagSlackChannelBundleTarget`

    One Bundle attached to one Slack channel. The Bundle can be used in that channel only.

    - `type: Literal["slack_channel"]`

    - `id: str`

      The Bundle Target's identifier. Starts with `btgt_`. No two Bundle Targets have the same one, and the same Bundle and target always give the same one, also after a detach and a new attach. It is opaque.

    - `created_at: datetime`

      Time the Bundle was attached.

      format: date-time

    - `slack_channel_id: str`

      The identifier of the Slack channel the Bundle is attached to, starting with `slch_`. It is the channel object's `id`, not Slack's `channel_id`.

  - `class BetaClaudeTagSlackWorkspaceBundleTarget`

    One Bundle attached to one Slack workspace. The Bundle can be used in the workspace and in every channel in it.

    - `type: Literal["slack_workspace"]`

    - `id: str`

      The Bundle Target's identifier. Starts with `btgt_`. No two Bundle Targets have the same one, and the same Bundle and target always give the same one, also after a detach and a new attach. It is opaque.

    - `created_at: datetime`

      Time the Bundle was attached.

      format: date-time

    - `slack_workspace_id: str`

      The identifier of the Slack workspace the Bundle is attached to, starting with `slws_`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_bundle_target = (
    client.beta.organization.claude_tag.bundles.targets.retrieve(
        target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
        bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
    )
)
print(beta_claude_tag_bundle_target)
```

##### Response (200)

```json
{
  "id": "id",
  "created_at": "2019-12-27T18:11:19.117Z",
  "slack_channel_id": "slack_channel_id",
  "type": "slack_channel"
}
```

### Detach Bundle

`beta.organization.claude_tag.bundles.targets.delete(target_id, **kwargs) -> BetaClaudeTagDeletedBundleTarget`

**DELETE** `/v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}`

Detach a Bundle from a Slack channel or a Slack workspace. A repeated detach returns 404.

#### Parameters

- `bundle_id: str` (path parameter)

  The Bundle's identifier, starting with `capp_`.

- `target_id: str` (path parameter)

  The Bundle Target's identifier, starting with `btgt_`. Attach Bundle and List Bundle Targets return it. It is never the identifier of the channel or workspace.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `experimental-claude-tag-2026-10-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

#### Returns

- `class BetaClaudeTagDeletedBundleTarget`

  Confirms that a Bundle was detached.

  - `type: Literal["bundle_target_deleted"]`

  - `id: str`

    The identifier the Bundle Target had.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_claude_tag_deleted_bundle_target = (
    client.beta.organization.claude_tag.bundles.targets.delete(
        target_id="btgt_01SvpyRQK3nN6eH9uhRA7n1qHq8TzW5mKc2YbX7vNd4RfJ",
        bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
    )
)
print(beta_claude_tag_deleted_bundle_target.id)
```

##### Response (200)

```json
{
  "id": "id",
  "type": "bundle_target_deleted"
}
```
