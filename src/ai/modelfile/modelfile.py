"""Generate and manage Ollama Modelfiles."""

import os
import tempfile

from .error import ModelfileError

"""
Build the complete Modelfile content.

The Modelfile structure is:
    FROM <base_model>

    <config_params (PARAMETER lines)>

    SYSTEM "
    <system_prompt>
    "

Args:
    base_model: The name of the base model (e.g., 'llama2').
    config_params: Multi-line string with PARAMETER directives.
    system_prompt: The system prompt text.

Returns:
    The complete Modelfile content as a string.

Raises:
    ModelfileError: If any required parameter is empty.
"""
def build_modelfile_content(
    base_model: str,
    config_params: str,
    system_prompt: str,
) -> str:
   
    if not base_model or not base_model.strip():
        raise ModelfileError("base_model cannot be empty")
    if not config_params or not config_params.strip():
        raise ModelfileError("config_params cannot be empty")
    if not system_prompt or not system_prompt.strip():
        raise ModelfileError("system_prompt cannot be empty")

    lines = [
        f"FROM {base_model}",
        "",
        config_params,
        "",
        'SYSTEM "',
        system_prompt,
        '"',
    ]
    content = "\n".join(lines)
    return content

"""
Write Modelfile content to a temporary file.

Uses `tempfile.NamedTemporaryFile` to create a secure temporary file.
The file is NOT deleted automatically (deletion is caller's responsibility).

Args:
    content: The Modelfile content to write.

Returns:
    The absolute path to the temporary file.

Raises:
    ModelfileError: If writing to the file fails.
"""
def write_temporary_modelfile(content: str) -> str:
    
    try:
        tmp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".Modelfile",
            delete=False,
            encoding="utf-8",
        )
        tmp_file.write(content)
        tmp_file.close()
        return tmp_file.name
    except IOError as e:
        raise ModelfileError(f"Failed to write temporary Modelfile: {e}") from e

"""
Delete a temporary Modelfile.

Args:
    file_path: The path to the Modelfile to delete.

Raises:
    ModelfileError: If deletion fails (other than file not found).
"""
def cleanup_modelfile(file_path: str) -> None:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError as e:
        raise ModelfileError(f"Failed to delete temporary Modelfile: {e}") from e